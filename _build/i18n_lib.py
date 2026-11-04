"""Internationalisation (EN | ES) for In Depth #93: catalogs, the English text the page ships with, and the checks that fail the build.

Sources of text, one place each:
  _build/i18n/en.json  editorial and interface text in English   (edit here)
  _build/i18n/es.json  the same keys in Spanish, plus the Spanish for the generated keys below   (edit here)
  doc.*                the docx blocks: English comes from the docx (paras93.json), Spanish from es.json
  mover.<id>           mover names: English comes from the Excel (data93.json), Spanish from es.json
Keys are stable names (chapter.s2.title, fig.ladder.caption, ...): they never depend on the wording of the text.
Values under doc.* and mover.* are plain text; every other value may carry inline html (<b>, <br>, <span>).
CLI:  python _build/i18n_lib.py            validates the catalogs (same as: python _build/build93.py _build . --check)."""
import html as H
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATED = ("doc.", "mover.")          # English text for these keys is not stored in en.json
PLAIN = GENERATED                       # values that are plain text (escaped when written into html)
KEY_RE = re.compile(r"^[a-z][A-Za-z0-9]*(\.[A-Za-z0-9_]+)+$")
SAME_AS_ENGLISH_OK = re.compile(r"^(abbr\.|brand\.|short\.asimo$|chart\.human\.walkFastSub$|mover\.(B0[1-7]|H0[1-4]|V0[1-2]|F0[1-7])$)")   # names and abbreviations that read the same in both languages


class CatalogError(Exception):
    pass


def load_catalog(path):
    """Reads a flat {key: text} json file; a repeated key is an error, not a silent override."""
    dups = []

    def pairs(items):
        d = {}
        for k, v in items:
            if k in d:
                dups.append(k)
            d[k] = v
        return d
    data = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs)
    if not isinstance(data, dict) or not all(isinstance(v, str) for v in data.values()):
        raise CatalogError(f"{path}: expected a flat object of strings")
    return data, dups


def esc(s):
    return H.escape(str(s), quote=False)


def placeholders(s):
    return set(re.findall(r"\{(\w+)\}", s))


def markup(s):
    """The tag skeleton of an html value: tag names in order, plus ids, so that a translation cannot drop a <b> or a placeholder span."""
    return [(m.group(1), tuple(re.findall(r'\bid="([^"]+)"', m.group(2)))) for m in re.finditer(r"<(/?\w+)([^>]*)>", s)]


def fmt_lead(text):
    """doc.s2b*: 'Humpback whale: 0.0020...' -> bold lead + the rest."""
    a, b = text.split(": ", 1)
    return f"<b>{esc(a + ':')}</b> {esc(b)}"


def render(catalog, key, args=None, fmt=None):
    """The html for one key, exactly as the page script writes it."""
    v = catalog[key]
    if fmt == "lead":
        return fmt_lead(v)
    for n, x in (args or {}).items():
        v = v.replace("{" + n + "}", str(x))
    return esc(v) if key.startswith(PLAIN) else v


def merge(en_src, generated_en):
    bad = [k for k in en_src if k.startswith(GENERATED)]
    if bad:
        raise CatalogError("en.json must not define generated keys (their English comes from the docx / Excel): " + ", ".join(bad[:8]))
    return {**en_src, **generated_en}


def scan_references(template_text, code_texts):
    """Keys the page refers to: data-i18n / data-i18n-attr in the template, t('key') calls and every key-shaped string literal in the code."""
    used, called = set(), set()
    for m in re.finditer(r'data-i18n="([^"]+)"', template_text):
        used.add(m.group(1)); called.add(m.group(1))
    for m in re.finditer(r'data-i18n-attr="([^"]+)"', template_text):
        for part in m.group(1).split(";"):
            k = part.split(":", 1)[1]; used.add(k); called.add(k)
    for text in code_texts:
        for m in re.finditer(r"""\b(?:t|tp|ta|K)\(\s*(['"])([^'"]+)\1\s*[,)]""", text):
            called.add(m.group(2)); used.add(m.group(2))
        for m in re.finditer(r"""(['"`])([a-z][A-Za-z0-9]*(?:\.[A-Za-z0-9_]+)+)\1""", text):
            used.add(m.group(2))
    return used, called


def validate(en, es, used, called, attr_keys=(), allow_unused=()):
    """Returns (errors, warnings). The build stops on errors."""
    errors, warnings = [], []
    for k in sorted(en):
        if not KEY_RE.match(k): errors.append(f"bad key name: {k}")
    for k in sorted(set(en) - set(es)): errors.append(f"missing in es.json: {k}")
    for k in sorted(set(es) - set(en)): errors.append(f"in es.json but not in the English catalog (renamed or removed?): {k}")
    for name, cat in (("EN", en), ("ES", es)):
        for k, v in sorted(cat.items()):
            if not v.strip(): errors.append(f"empty {name} text: {k}")
    for k in sorted(set(en) & set(es)):
        if placeholders(en[k]) != placeholders(es[k]): errors.append(f"placeholders differ ({k}): EN {sorted(placeholders(en[k]))} vs ES {sorted(placeholders(es[k]))}")
        if not k.startswith(PLAIN) and markup(en[k]) != markup(es[k]): errors.append(f"html markup differs ({k}): EN {markup(en[k])} vs ES {markup(es[k])}")
        if k.startswith("doc.s2b") and (": " not in en[k] or ": " not in es[k]): errors.append(f"{k}: the bold lead needs 'label: text' in both languages")
        if en[k] == es[k] and not SAME_AS_ENGLISH_OK.match(k) and len(en[k]) > 12: warnings.append(f"ES equals EN (untranslated?): {k}")
    for k in sorted(called - set(en)): errors.append(f"key used by the page but not defined: {k}")
    for k in sorted(set(en) - used - set(allow_unused)):
        if not k.startswith(GENERATED): errors.append(f"key defined but never used: {k}")
    for k in sorted(attr_keys):
        for name, cat in (("EN", en), ("ES", es)):
            if k in cat and re.search(r"[<&]", cat[k]): errors.append(f"{name} text for attribute key {k} must be plain text (no tags or entities)")
    seen = {}
    for k, v in en.items():
        if len(v) > 14 and not k.startswith(GENERATED): seen.setdefault(v, []).append(k)
    for v, ks in seen.items():
        if len(ks) > 1: warnings.append(f"same English text under several keys: {ks}")
    return errors, warnings


def attr_keys_in(template_text):
    out = set()
    for m in re.finditer(r'data-i18n-attr="([^"]+)"', template_text):
        for part in m.group(1).split(";"): out.add(part.split(":", 1)[1])
    return out


def main():
    """CLI: runs the build's catalog checks (they need the docx and the Excel for the generated keys) without writing anything."""
    import subprocess
    return subprocess.run([sys.executable, "-X", "utf8", str(HERE / "build93.py"), str(HERE), str(HERE.parent), "--check"]).returncode


if __name__ == "__main__":
    sys.exit(main())
