"""i18n tests that need no browser: the catalog checks, and the build refusing bad catalogs.
Run from the project folder:  python -m unittest discover -s tests -v"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
sys.path.insert(0, str(BUILD))
import i18n_lib as I18  # noqa: E402


class Checks(unittest.TestCase):
    """The rules in i18n_lib.validate, one failure at a time, on small catalogs."""
    EN = {"a.title": "Hello <b>world</b>", "a.count": "{n} items", "a.note": "Plain"}
    ES = {"a.title": "Hola <b>mundo</b>", "a.count": "{n} elementos", "a.note": "Simple"}
    USED = {"a.title", "a.count", "a.note"}

    def run_validate(self, en=None, es=None, used=None, called=None, attr=()):
        return I18.validate(en or self.EN, es or self.ES, used if used is not None else self.USED, called if called is not None else self.USED, attr)

    def test_clean_catalogs_pass(self):
        errors, _ = self.run_validate()
        self.assertEqual(errors, [])

    def test_key_missing_in_spanish(self):
        errors, _ = self.run_validate(es={k: v for k, v in self.ES.items() if k != "a.note"})
        self.assertTrue(any("missing in es.json: a.note" in e for e in errors), errors)

    def test_key_only_in_spanish(self):
        errors, _ = self.run_validate(es={**self.ES, "a.extra": "Sobra"})
        self.assertTrue(any("not in the English catalog" in e and "a.extra" in e for e in errors), errors)

    def test_empty_translation(self):
        errors, _ = self.run_validate(es={**self.ES, "a.note": "  "})
        self.assertTrue(any("empty ES text: a.note" in e for e in errors), errors)

    def test_placeholder_dropped(self):
        errors, _ = self.run_validate(es={**self.ES, "a.count": "elementos"})
        self.assertTrue(any("placeholders differ (a.count)" in e for e in errors), errors)

    def test_markup_dropped(self):
        errors, _ = self.run_validate(es={**self.ES, "a.title": "Hola mundo"})
        self.assertTrue(any("html markup differs (a.title)" in e for e in errors), errors)

    def test_key_used_but_undefined(self):
        errors, _ = self.run_validate(called=self.USED | {"a.ghost"})
        self.assertTrue(any("used by the page but not defined: a.ghost" in e for e in errors), errors)

    def test_key_defined_but_unused(self):
        errors, _ = self.run_validate(used={"a.title", "a.count"})
        self.assertTrue(any("never used: a.note" in e for e in errors), errors)

    def test_bad_key_name(self):
        errors, _ = I18.validate({"Bad key": "x"}, {"Bad key": "y"}, {"Bad key"}, set())
        self.assertTrue(any("bad key name" in e for e in errors), errors)

    def test_attribute_text_must_be_plain(self):
        errors, _ = self.run_validate(attr={"a.title"})
        self.assertTrue(any("must be plain text" in e for e in errors), errors)

    def test_duplicate_keys_in_a_file_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            p.write_text('{"a.b": "one", "a.b": "two"}', encoding="utf-8")
            data, dups = I18.load_catalog(p)
            self.assertEqual(dups, ["a.b"])

    def test_generated_keys_cannot_live_in_en_json(self):
        with self.assertRaises(I18.CatalogError):
            I18.merge({"doc.s1p1": "x"}, {})

    def test_render_escapes_plain_keys_only(self):
        cat = {"doc.x": "a < b & c", "ui.x": "a <b>b</b>", "ui.n": "{n} items"}
        self.assertEqual(I18.render(cat, "doc.x"), "a &lt; b &amp; c")
        self.assertEqual(I18.render(cat, "ui.x"), "a <b>b</b>")
        self.assertEqual(I18.render(cat, "ui.n", {"n": 3}), "3 items")
        self.assertEqual(I18.fmt_lead("Whale: 0.003, derived"), "<b>Whale:</b> 0.003, derived")


class Catalogs(unittest.TestCase):
    """The real catalogs."""

    @classmethod
    def setUpClass(cls):
        cls.en, cls.dup_en = I18.load_catalog(BUILD / "i18n" / "en.json")
        cls.es, cls.dup_es = I18.load_catalog(BUILD / "i18n" / "es.json")

    def test_no_duplicate_keys(self):
        self.assertEqual((self.dup_en, self.dup_es), ([], []))

    def test_en_json_holds_no_generated_keys(self):
        self.assertEqual([k for k in self.en if k.startswith(I18.GENERATED)], [])

    def test_every_hand_written_key_exists_in_both_languages(self):
        es_hand = {k for k in self.es if not k.startswith(I18.GENERATED)}
        self.assertEqual(set(self.en) - es_hand, set())
        self.assertEqual(es_hand - set(self.en) - {k for k in es_hand if k.startswith("doc.kfig.")}, set())

    def test_cli_validation_passes(self):
        r = subprocess.run([sys.executable, "-X", "utf8", str(BUILD / "i18n_lib.py")], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_mover_in_the_data_has_a_spanish_name(self):
        data = json.loads((BUILD / "data93.json").read_text(encoding="utf-8"))
        ids = {d["id"] for s in ("ladder", "living", "human", "robots", "people", "goods", "goods_whole") for d in data[s] if not d["mover"].endswith("(reference)")}
        self.assertEqual({i for i in ids if f"mover.{i}" not in self.es}, set())

    def test_every_docx_block_has_a_spanish_text(self):
        paras = json.loads((BUILD / "paras93.json").read_text(encoding="utf-8"))["paras"]
        keys = {f"doc.{k}" for k in paras if not k.startswith("src") and not k.endswith("_h")} | {"doc.cover_sub"}
        self.assertEqual({k for k in keys if k not in self.es}, set())

    def test_spanish_uses_decimal_commas_in_hand_written_numbers(self):
        # a decimal point between digits in Spanish text is almost always an English leftover (the page script adds the comma to chart numbers)
        for k, v in self.es.items():
            if k.startswith(("mover.", "boundary.")): continue
            self.assertFalse(re.search(r"(?<![\w.])\d\.\d", re.sub(r"https?://\S+|<[^>]+>", "", v)) and not k.startswith("meta."), f"{k}: {v[:80]}")


class BuildGate(unittest.TestCase):
    """The build must refuse bad catalogs and must not write the page when it does."""

    def build(self, mutate=None):
        tmp = Path(tempfile.mkdtemp(prefix="indepth93-build-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        shutil.copytree(BUILD, tmp / "_build", ignore=shutil.ignore_patterns("__pycache__", "*92*", "es_missing.txt", "data.json", "paras.json", "docx_paras.py", "prep_data.py"))
        if mutate: mutate(tmp / "_build")
        r = subprocess.run([sys.executable, "-X", "utf8", str(tmp / "_build" / "build93.py"), str(tmp / "_build"), str(tmp)], capture_output=True, text=True, encoding="utf-8")
        return r, tmp

    def edit_es(self, fn):
        def mutate(b):
            p = b / "i18n" / "es.json"; d = json.loads(p.read_text(encoding="utf-8")); fn(d)
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        return mutate

    def test_good_build_succeeds_and_is_reproducible(self):
        r1, t1 = self.build(); r2, t2 = self.build()
        self.assertEqual(r1.returncode, 0, r1.stdout + r1.stderr)
        self.assertEqual((t1 / "index_93.html").read_text(encoding="utf-8"), (t2 / "index_93.html").read_text(encoding="utf-8"))
        page = (t1 / "index_93.html").read_text(encoding="utf-8")
        self.assertIn("GENERATED by _build/build93.py", page)
        self.assertEqual((t1 / "index_93.html").read_bytes(), (t1 / "index.html").read_bytes())

    def test_missing_spanish_key_fails_and_writes_nothing(self):
        r, tmp = self.build(self.edit_es(lambda d: d.pop("fig.ladder.caption")))
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing in es.json: fig.ladder.caption", r.stdout)
        self.assertFalse((tmp / "index_93.html").exists())

    def test_missing_docx_translation_fails(self):
        r, _ = self.build(self.edit_es(lambda d: d.pop("doc.s6p2")))
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing in es.json: doc.s6p2", r.stdout)

    def test_missing_mover_name_fails(self):
        r, _ = self.build(self.edit_es(lambda d: d.pop("mover.F07")))
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing in es.json: mover.F07", r.stdout)

    def test_dropped_placeholder_fails(self):
        r, _ = self.build(self.edit_es(lambda d: d.update({"sources.summary": "fuentes · cierre de la investigación"})))
        self.assertEqual(r.returncode, 1)
        self.assertIn("placeholders differ (sources.summary)", r.stdout)

    def test_duplicate_key_in_catalog_fails(self):
        def mutate(b):
            p = b / "i18n" / "es.json"; t = p.read_text(encoding="utf-8")
            p.write_text(t.rstrip().rstrip("}").rstrip() + ',\n  "ui.language": "Idioma otra vez"\n}', encoding="utf-8")
        r, _ = self.build(mutate)
        self.assertEqual(r.returncode, 1)
        self.assertIn("duplicate key in es.json: ui.language", r.stdout)

    def test_unused_key_fails(self):
        def mutate(b):
            for lang in ("en", "es"):
                p = b / "i18n" / f"{lang}.json"; d = json.loads(p.read_text(encoding="utf-8")); d["zz.unused"] = "Unused"; p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        r, _ = self.build(mutate)
        self.assertEqual(r.returncode, 1)
        self.assertIn("key defined but never used: zz.unused", r.stdout)

    def test_key_used_by_template_but_undefined_fails(self):
        def mutate(b):
            p = b / "body93.html"; t = p.read_text(encoding="utf-8")
            p.write_text(t.replace('data-i18n="cover.tag"', 'data-i18n="cover.nothing"', 1), encoding="utf-8")
        r, _ = self.build(mutate)
        self.assertEqual(r.returncode, 1)
        self.assertIn("used by the page but not defined: cover.nothing", r.stdout)

    def test_english_in_generated_namespace_is_refused(self):
        def mutate(b):
            p = b / "i18n" / "en.json"; d = json.loads(p.read_text(encoding="utf-8")); d["doc.sum1"] = "Overridden"; p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        r, _ = self.build(mutate)
        self.assertEqual(r.returncode, 1)
        self.assertIn("en.json must not define generated keys", r.stdout)

    def test_text_left_in_the_template_is_refused(self):
        def mutate(b):
            p = b / "body93.html"; t = p.read_text(encoding="utf-8")
            p.write_text(t.replace('<span class="cover__tag" data-i18n="cover.tag"></span>', '<span class="cover__tag" data-i18n="cover.tag">Hand-written</span>', 1), encoding="utf-8")
        r, _ = self.build(mutate)
        self.assertEqual(r.returncode, 1)
        self.assertIn("must hold no text", r.stdout)


class BuiltPage(unittest.TestCase):
    """The generated page carries both catalogs and the same data as the sources."""

    @classmethod
    def setUpClass(cls):
        page = (ROOT / "index_93.html").read_text(encoding="utf-8")
        cls.page = page
        cls.data = json.loads((BUILD / "data93.json").read_text(encoding="utf-8"))
        m = re.search(r"^const I18N = (\{.*\});", page, flags=re.M)
        cls.i18n = json.loads(m.group(1).replace("<\\/", "</"))
        m = re.search(r"^const DATA = (\{.*\});", page, flags=re.M)
        cls.embedded = json.loads(m.group(1))

    def test_page_data_is_the_excel_data(self):
        self.assertEqual(self.embedded, self.data)

    def test_catalogs_in_the_page_have_the_same_keys(self):
        self.assertEqual(set(self.i18n["en"]), set(self.i18n["es"]))

    def test_page_ships_no_hand_written_text_outside_catalog_elements(self):
        # every visible text node of the template sits in an element that carries a data-i18n key (or is a number/brand/unit)
        from html.parser import HTMLParser
        VOID = {"img", "br", "meta", "link", "input", "hr", "source", "path", "line", "circle", "rect", "ellipse", "stop"}
        left, stack = [], []

        class Scan(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag in VOID: return
                a = dict(attrs)
                stack.append((tag, "data-i18n" in a or a.get("lang") == "en"))   # keyed elements and the English sources list own their text

            def handle_startendtag(self, tag, attrs): pass

            def handle_endtag(self, tag):
                while stack and stack[-1][0] != tag: stack.pop()
                if stack: stack.pop()

            def handle_data(self, data):
                if any(owned for _, owned in stack) or any(t in ("script", "style") for t, _ in stack): return
                if re.search(r"[A-Za-z]{3}", data) and data.strip() not in ("EN", "ES"): left.append(data.strip())
        Scan().feed(re.search(r"<body>(.*?)<script src", self.page, flags=re.S).group(1))
        self.assertEqual(left, [])

    def test_html_lang_and_head_come_from_the_catalog(self):
        self.assertIn('<html lang="en">', self.page)
        self.assertIn(f"<title>{self.i18n['en']['meta.title']}</title>", self.page)
        self.assertIn(self.i18n["en"]["meta.description"], self.page)


if __name__ == "__main__":
    unittest.main()
