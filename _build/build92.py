"""Builds index_92.html from the files in _build/ (self-contained: no dependency on the #91 page).
Usage (from the project folder):  python -X utf8 _build/build92.py _build .
Fails (exit code 1) if any docx block is missing, duplicated or altered beyond the edits listed in EDITS."""
import json, sys, re, html as H

S, PROJ = sys.argv[1], sys.argv[2]
read = lambda name: open(f"{S}/{name}", encoding="utf-8").read()

HEAD = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>More Plugs than Pumps | Astara Intelligence In Depth #92</title>
<meta name="description" content="Public charging points, fuel stations and the fleets they serve in 40 markets. Astara Intelligence In Depth #92.">
<meta name="theme-color" content="#221E41">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="deploy/img/hero-1672.webp" imagesrcset="deploy/img/hero-840.webp 840w, deploy/img/hero-1672.webp 1672w" imagesizes="100vw">
<style>
"""

css, body, js = read("style92.css"), read("body92.html"), read("app92.js").replace("/*__DATA__*/null", read("data.json"))
P = json.load(open(f"{S}/paras.json", encoding="utf-8"))
raw = dict(P["paras"])
e = lambda s: H.escape(str(s), quote=False)

# ---- editorial edits on top of the docx text: every one must apply exactly once ----
# [EXT: ...] markers are source tags for the editor; the sources go to captions and the Sources list.
# The other three remove notes addressed to the designer ("the piece should ...") and an internal reference.
EXT = re.compile(r" ?\[EXT(?:: [^\]]*)?\]")
EDITS = [
    ("s6p1", ", and the piece should say so plainly:", ":"),
    ("s6p2", ", and the piece should not guess a cause.", "."),
    ("s7b2", " (source Excel)", ""),
]
paras = {k: EXT.sub("", v) for k, v in raw.items()}
n_ext = sum(len(EXT.findall(v)) for v in raw.values())
for k, old, new in EDITS:
    assert paras[k].count(old) == 1, (k, old)
    paras[k] = paras[k].replace(old, new)
print(f"edits: {n_ext} [EXT] markers removed; {len(EDITS)} text edits ({', '.join(k for k, _, _ in EDITS)})")

# bullets whose lead word(s) become a bold label: "Europe: ..." / "Unit. ..."
def lead_html(k, sep):
    a, b = paras[k].split(sep, 1)
    return f"<b>{e(a + sep.strip())}</b> {e(b)}"
HTML = {k: lead_html(k, ": ") for k in paras if re.fullmatch(r"s3b\d", k)}
HTML.update({k: lead_html(k, ". ") for k in paras if re.fullmatch(r"s6b\d", k)})

# ---- V01 key figures: the docx "Key figures" table, verbatim ----
kf = next(t for t in P["tables"] if t["section"] == "sum" and t["rows"][0][:2] == ["Figure", "Value"])
cls = lambda fig: "kfig__c--pump" if "Fuel" in fig else ("kfig__c--ev" if "Electric" in fig else "")
tiles = "".join(f'<div class="kfig__c {cls(f)}"><div class="kfig__v">{e(v)}</div><div class="kfig__l">{e(f)}</div>'
                f'<div class="kfig__s">{e(r)} · {e(EXT.sub("", s).strip())}</div></div>' for f, v, r, s in kf["rows"][1:])
assert len(kf["rows"]) == 7
body = body.replace("[[KEY_FIGURES]]", f'<div class="kfig">{tiles}</div>')

# ---- Sources (Appendix B). The editor's internal workbook is not a public source. ----
srcs = []
for k in sorted((k for k in paras if k.startswith("src")), key=lambda k: int(k[3:])):
    t = paras[k]
    if t.startswith("Source workbook supplied by the editor"): continue
    m = re.match(r"(.*) \(([^()]*(?:\([^()]*\)[^()]*)*)\)\. (https?://\S+)$", t); assert m, t
    name, date, url = m.groups()
    dom = re.sub(r"^www\d*\.", "", url.split("/")[2])
    srcs.append(f'<li>{e(name)} <small>({e(date)})</small> · <a href="{H.escape(url)}" target="_blank" rel="noopener">{e(dom)}</a></li>')
body = body.replace("[[SOURCES]]", "<ol>" + "".join(srcs) + "</ol>").replace("[[SOURCES_COUNT]]", str(len(srcs)))


ICONS = {
    "unit": '<svg viewBox="0 0 24 24"><rect x="3" y="7" width="7" height="13" rx="1.5"/><path d="M6.5 11v3"/><rect x="14" y="4" width="7" height="16" rx="1.5"/><path d="M16 8h3M16 11h3"/></svg>',
    "time": '<svg viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/></svg>',
    "home": '<svg viewBox="0 0 24 24"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M12 13l-2 3h4l-2 3"/></svg>',
}
for k, v in ICONS.items(): body = body.replace(f"[[ICON:{k}]]", v)

# flag tiles (deploy/flags, flag-icons 1x1, MIT): [[FLAGS:it,de,es]]
body = re.sub(r"\[\[FLAGS:([a-z,]+)\]\]", lambda m: '<span class="facts__f" aria-hidden="true">' + ''.join(
    f'<span class="flag" style="background-image:url(deploy/flags/{c}.svg)"></span>' for c in m.group(1).split(',')) + '</span>', body)

used = set()
def sub(m):
    k = m.group(1); used.add(k)
    return HTML.get(k) or e(paras[k])
body = re.sub(r"\{\{([a-z0-9_]+)\}\}", sub, body)
assert "{{" not in body and "[[" not in body

page = HEAD + css + "</style>\n</head>\n<body>\n\n" + body + \
    '\n<script src="deploy/d3.v7.min.js"></script>\n<script src="deploy/topojson-client.min.js"></script>\n<script src="deploy/countries-110m.js"></script>\n<script>\n' + js + "\n</script>\n\n</body></html>\n"
open(f"{PROJ}/index_92.html", "w", encoding="utf-8").write(page)
open(f"{PROJ}/index.html", "w", encoding="utf-8").write(page)   # GitHub Pages serves index.html at the site root

# ---- verification: every docx block used exactly once and unaltered (after EDITS); excerpts literal ----
fail = []
blocks = [k for k in P["paras"] if not k.startswith("src") and not k.endswith("_h")]
missing = [k for k in blocks if k not in used]
print("docx blocks:", len(blocks), "missing:", missing)
if missing: fail.append("missing blocks")
cnt = {k: len(re.findall(r'data-src="%s"' % k, body)) for k in blocks}
bad = {k: v for k, v in cnt.items() if v != 1}
print("data-src markers not exactly once:", bad)
if bad: fail.append("markers")
norm = lambda s: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
for k in blocks:
    seg = re.search(r'data-src="%s"[^>]*>(.*?)</(?:p|li)>' % k, body, flags=re.S)
    if not (seg and norm(seg.group(1)) == norm(e(paras[k]))):
        print("MISMATCH", k); fail.append("mismatch " + k)
fulln = norm(" ".join(paras[k] for k in blocks))
for ex in re.findall(r'class="[^"]*excerpt-text[^"]*">(.*?)</', body):
    ok = norm(ex) in fulln
    print("excerpt OK" if ok else "EXCERPT NOT IN DOCX", "|", norm(ex)[:70])
    if not ok: fail.append("excerpt")
print("sources listed:", len(srcs))
print(len(page), "bytes written")
if fail:
    print("BUILD CHECK FAILED:", fail); sys.exit(1)
