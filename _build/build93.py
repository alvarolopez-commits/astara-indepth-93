"""Builds index_93.html from the files in _build/ (self-contained: no dependency on the #92 page).
Usage (from the project folder):  python -X utf8 _build/build93.py _build .
Fails (exit code 1) if any docx block is missing, duplicated or altered beyond the edits listed in EDITS."""
import json, math, sys, re, html as H

S, PROJ = sys.argv[1], sys.argv[2]
read = lambda name: open(f"{S}/{name}", encoding="utf-8").read()

HEAD = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Cheapest Kilometre on Earth | Astara Intelligence In Depth #93</title>
<meta name="description" content="Whales, eels, cyclists, robots, ships and drones on one energy scale. Astara Intelligence In Depth #93.">
<meta name="theme-color" content="#221E41">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="deploy/img/hero-1672.webp" imagesrcset="deploy/img/hero-840.webp 840w, deploy/img/hero-1672.webp 1672w" imagesizes="100vw">
<style>
"""

DATA = json.load(open(f"{S}/data93.json", encoding="utf-8"))
css, body = read("style93.css"), read("body93.html")
js = read("app93.js").replace("/*__DATA__*/null", read("data93.json"))
ES = {}
exec(read("es93.py"), ES)           # P: Spanish for each docx block, UI: Spanish for every other text (keyed by the English text)
ES_P, ES_UI = ES["P"], ES["UI"]
ui_missing = []
P = json.load(open(f"{S}/paras93.json", encoding="utf-8"))
raw = dict(P["paras"])
e = lambda s: H.escape(str(s), quote=False)

# ---- editorial edits on top of the docx text: every one must apply exactly once ----
# [EXT: ...] markers are source tags for the editor; the sources go to captions and the Sources list.
EXT = re.compile(r" ?\[EXT(?:: [^\]]*)?\]")
EDITS = [   # references to the editor's files, which are not published
    ("how4", ", with its URL in Appendix B and in the Excel.", ", and every source is listed with its URL at the end of the page."),
    ("s1p2", "The conversions are in sheet 10_Formula and each row shows its inputs.", "Each row shows its inputs."),
]
paras = {k: EXT.sub("", v) for k, v in raw.items()}
n_ext = sum(len(EXT.findall(v)) for v in raw.values())
for k, old, new in EDITS:
    assert paras[k].count(old) == 1, (k, old)
    paras[k] = paras[k].replace(old, new)
print(f"edits: {n_ext} [EXT] markers removed; {len(EDITS)} text edits")
paras["cover_sub"] = P["cover"][0]          # the cover strapline

# bullets whose lead word(s) become a bold label: "Humpback whale: ..."
def lead_html(k, sep):
    a, b = paras[k].split(sep, 1)
    return f"<b>{e(a + sep.strip())}</b> {e(b)}"
HTML = {k: lead_html(k, ": ") for k in paras if re.fullmatch(r"s2b\d", k)}

# ---- icons: 100x100 line drawings of the movers (cover and champions strip) ----
MOVERS = {
    "whale": '<path d="M8 56C8 42 26 34 48 35c16 1 27 9 38 15"/><path d="M86 50 95 36M86 50 97 62"/><path d="M86 50C76 62 60 70 42 70 22 70 8 68 8 56"/><path d="M34 62c6 3 13 2 18-3"/><circle cx="22" cy="54" r="1.8" fill="currentColor" stroke="none"/><path d="M40 28c0-5 4-7 4-12M47 28c0-5 4-7 4-12"/>',
    "eel": '<path d="M6 64C16 42 28 42 38 60S58 80 68 60 84 40 94 52"/><circle cx="90.5" cy="49" r="1.8" fill="currentColor" stroke="none"/><path d="M62 70c3 7 9 8 12 1"/>',
    "bike": '<circle cx="24" cy="68" r="15"/><circle cx="76" cy="68" r="15"/><path d="M24 68H46L40 46H66L76 68M46 68 66 46M34 41H46M66 46 62 37H72"/><circle cx="50" cy="22" r="6"/><path d="M49 29 41 45M49 29 63 37"/>',
    "car": '<path d="M6 68C8 54 30 46 56 46c22 0 38 10 38 22Z"/><path d="M37 49c5-10 22-11 31-1"/><circle cx="26" cy="70" r="7"/><circle cx="76" cy="70" r="7"/>',
    "ship": '<path d="M6 62H94L84 80H18Z"/><rect x="22" y="46" width="16" height="14"/><rect x="40" y="46" width="16" height="14"/><rect x="58" y="46" width="16" height="14"/><rect x="31" y="32" width="16" height="14"/><rect x="49" y="32" width="16" height="14"/><path d="M80 62V42H90V62"/><path d="M10 90q6-6 12 0t12 0 12 0 12 0 12 0 12 0"/>',
    "walker": '<circle cx="50" cy="16" r="8"/><path d="M50 26V56M50 34 36 47M50 34 64 45M50 56 38 84M50 56 62 70 58 86"/>',
    "robot": '<rect x="38" y="10" width="24" height="18" rx="5"/><path d="M50 10V4"/><circle cx="44" cy="19" r="1.8" fill="currentColor" stroke="none"/><circle cx="56" cy="19" r="1.8" fill="currentColor" stroke="none"/><rect x="32" y="34" width="36" height="28" rx="6"/><path d="M32 40 20 58M68 40 80 58M42 62V86H34M58 62V86H66"/>',
    "drone": '<rect x="40" y="42" width="20" height="10" rx="3"/><path d="M40 45 20 34M60 45 80 34M40 50 20 62M60 50 80 62"/><ellipse cx="16" cy="32" rx="12" ry="3"/><ellipse cx="84" cy="32" rx="12" ry="3"/><ellipse cx="16" cy="64" rx="12" ry="3"/><ellipse cx="84" cy="64" rx="12" ry="3"/><path d="M50 52V64"/><rect x="43" y="64" width="14" height="13" rx="2"/>',
}
mover_svg = lambda k, cls="": f'<svg class="{cls}" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{MOVERS[k]}</svg>'

ICONS = {   # 24x24 line icons (How to read cards)
    "ruler": '<svg viewBox="0 0 24 24"><rect x="2" y="8" width="20" height="8" rx="1.5"/><path d="M6 8v3M10 8v4M14 8v3M18 8v4"/></svg>',
    "bases": '<svg viewBox="0 0 24 24"><circle cx="8" cy="12" r="5"/><circle cx="16.5" cy="12" r="5" stroke-dasharray="2 2.4"/></svg>',
    "bolt": '<svg viewBox="0 0 24 24"><path d="M13 2 5 13.5h6L10 22l9-12h-6.5Z"/></svg>',
    "doc": '<svg viewBox="0 0 24 24"><path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
}
for k, v in ICONS.items(): body = body.replace(f"[[ICON:{k}]]", v)

# group colour class per champion (matches the chart palette)
GROUP = {"Humpback whale": ("live", "whale"), "European eel": ("live", "eel"), "Human on a bicycle": ("human", "bike"),
         "Shell Eco-marathon prototype": ("people", "car"), "Ocean freight ship": ("goods", "ship"),
         "Cornell Ranger (legged robot)": ("robot", "robot")}

# ---- V01 champions strip: the docx "Key figures" table, verbatim ----
kf = next(t for t in P["tables"] if t["section"] == "sum" and t["rows"][0][:2] == ["Class", "Champion"])
assert len(kf["rows"]) == 7
tiles = ""
for cls_, champ, cot, basis, grade in kf["rows"][1:]:
    g, ic = GROUP[champ]
    tiles += (f'<div class="kfig__c kfig__c--{g}"><div class="kfig__ic">{mover_svg(ic)}</div>'
              f'<div class="kfig__k">{e(cls_)}</div><div class="kfig__v">{e(cot)}</div><div class="kfig__l">{e(champ)}</div>'
              f'<div class="kfig__s">{e(basis)} · Grade {e(grade)}</div></div>')
body = body.replace("[[KEY_FIGURES]]", f'<div class="kfig">{tiles}</div>')

# ---- Sources (Appendix B). The editor's internal workbook is not a public source. ----
srcs = []
for k in sorted((k for k in paras if k.startswith("src")), key=lambda k: int(k[3:])):
    t = paras[k]
    if not re.search(r"\. https?://\S+$", t): continue          # internal file references (editor's workbook)
    m = re.match(r"(.*) \(([^()]*(?:\([^()]*\)[^()]*)*)\)\. (https?://\S+)$", t); assert m, t
    name, date, url = m.groups()
    dom = re.sub(r"^www\d*\.", "", url.split("/")[2])
    srcs.append(f'<li>{e(name)} <small>({e(date)})</small> · <a href="{H.escape(url)}" target="_blank" rel="noopener">{e(dom)}</a></li>')
body = body.replace("[[SOURCES]]", "<ol>" + "".join(srcs) + "</ol>").replace("[[SOURCES_COUNT]]", str(len(srcs)))

# ---- cover art: eight movers climbing the log COT scale (positions are computed from the data) ----
# two compositions of the same drawing, shown as a figure under the cover: a wide band for desktop and a compact one for phones
ART_ARIA = "Eight movers on a rising curve of cost of transport, from the humpback whale at 0.003 to a delivery drone at 16"
ART_AXIS = "COST OF TRANSPORT · LOG SCALE · LOWER IS BETTER"
L = {d["id"]: d for d in DATA["ladder"]}
CHAIN = [("L01", "whale", "Whale", "live"), ("V01", "car", "Eco car", "people"), ("F01", "ship", "Ship", "goods"),
         ("L02", "eel", "Eel", "live"), ("H04", "bike", "Cyclist", "human"), ("H01", "walker", "Walker", "human"),
         ("B04", "robot", "ASIMO", "robot"), ("F07", "drone", "Drone", "goods")]
COL = {"live": "#3EC6C6", "human": "#8BCDFF", "robot": "#B79CFF", "people": "#FFB935", "goods": "#FF8F9C"}
ART_G = '<g fill="none" stroke="currentColor" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">'
def cot_txt(v): return f"{v:.4f}" if v < .01 else (f"{v:.3f}" if v < 1 else (f"{v:.2f}" if v < 10 else f"{v:.1f}"))
def smooth(p):          # Catmull-Rom through the points, as cubic Beziers
    d = f"M{p[0][0]:.0f} {p[0][1]:.0f}"
    for i in range(len(p) - 1):
        a, b, c, dd = p[max(i - 1, 0)], p[i], p[i + 1], p[min(i + 2, len(p) - 1)]
        d += f" C{b[0] + (c[0] - a[0]) / 6:.0f} {b[1] + (c[1] - a[1]) / 6:.0f} {c[0] - (dd[0] - b[0]) / 6:.0f} {c[1] - (dd[1] - b[1]) / 6:.0f} {c[0]:.0f} {c[1]:.0f}"
    return d
def cover_art(cls, W, H, x0, step, ybase, yb, ytop, r, k, fs, preserve, uid):
    lo, hi = math.log10(L["L01"]["cot"]), math.log10(L["F07"]["cot"])
    pts = [(x0 + i * step, yb - (math.log10(L[i_]["cot"]) - lo) / (hi - lo) * (yb - ytop)) for i, (i_, *_r) in enumerate(CHAIN)]
    a = [f'<svg class="info__art {cls}" viewBox="0 0 {W} {H}" preserveAspectRatio="{preserve}" role="img" aria-label="{ART_ARIA}" data-aria="{ART_ARIA}">',
         f'<defs><radialGradient id="cg1{uid}" cx="70%" cy="35%" r="60%"><stop offset="0" stop-color="#1A4D7A" stop-opacity=".55"/><stop offset="1" stop-color="#221E41" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="cg2{uid}" x1="0" x2="1"><stop offset="0" stop-color="#8BCDFF" stop-opacity=".2"/><stop offset=".3" stop-color="#8BCDFF" stop-opacity=".6"/><stop offset="1" stop-color="#FFB935" stop-opacity=".85"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="#221E41"/><rect width="{W}" height="{H}" fill="url(#cg1{uid})"/>']
    g = round(W / 14)
    for gx in range(0, W, g): a.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="#DCE5ED" stroke-opacity=".035"/>')
    for gy in range(round(g / 2), H, g): a.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="#DCE5ED" stroke-opacity=".035"/>')
    a.append(f'<line x1="{x0 - step / 2:.0f}" y1="{ybase}" x2="{x0 + 7 * step + step / 2:.0f}" y2="{ybase}" stroke="#DCE5ED" stroke-opacity=".35"/>')
    a.append(f'<path d="{smooth(pts)}" fill="none" stroke="url(#cg2{uid})" stroke-width="{3 * k / .76:.1f}" stroke-dasharray="2 {9 * k / .76:.0f}" stroke-linecap="round"/>')
    for (id_, ic, nm, grp), (px, py) in zip(CHAIN, pts):
        c = COL[grp]
        a.append(f'<line x1="{px:.0f}" y1="{py + r + 6:.0f}" x2="{px:.0f}" y2="{ybase}" stroke="{c}" stroke-opacity=".4" stroke-dasharray="3 6"/>')
        a.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r}" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".55"/>')
        a.append(f'<g transform="translate({px - 50 * k:.0f} {py - 50 * k:.0f}) scale({k})" style="color:{c}">{ART_G % (3.6 / k * .76)}{MOVERS[ic]}</g></g>')
        a.append(f'<circle cx="{px:.0f}" cy="{ybase}" r="{fs[0] / 5:.1f}" fill="{c}"/>')
        a.append(f'<text x="{px:.0f}" y="{ybase + fs[0] * 1.7:.0f}" text-anchor="middle" font-size="{fs[0]}" font-weight="700" fill="#FFFFFF" data-num="{cot_txt(L[id_]["cot"])}">{cot_txt(L[id_]["cot"])}</text>')
        a.append(f'<text x="{px:.0f}" y="{ybase + fs[0] * 1.7 + fs[1] * 1.45:.0f}" text-anchor="middle" font-size="{fs[1]}" font-weight="500" fill="#A9BCCB" data-t>{nm}</text>')
        ui_missing.append(nm)
    a.append(f'<text x="{W / 2:.0f}" y="{ybase + fs[0] * 1.7 + fs[1] * 1.45 + fs[2] * 2.3:.0f}" text-anchor="middle" font-size="{fs[2]}" font-weight="700" letter-spacing="2" fill="#89A1B4" data-t>{ART_AXIS}</text>')
    ui_missing.extend([ART_AXIS, ART_ARIA])
    return "".join(a) + '</svg>'
body = body.replace("[[INFOGRAPHIC]]",
    cover_art("info__art--band", 1672, 470, 241, 170, 352, 300, 96, 56, .78, (24, 17, 13), "xMidYMid meet", "b") +
    cover_art("info__art--stack", 900, 620, 70, 108, 392, 330, 96, 38, .52, (22, 16, 11), "xMidYMid meet", "s"))

used = set()
def sub(m):
    k = m.group(1); used.add(k)
    return HTML.get(k) or e(paras[k])
body = re.sub(r"\{\{([a-z0-9_]+)\}\}", sub, body)
assert "{{" not in body and "[[" not in body

# ---- Spanish layer: tag every translatable element; the browser swaps its html for ES_UI[english html] ----
def tag_page(b):
    got = []
    def one(tag, cls):
        nonlocal b
        pat = (rf'<{tag} (class="[^"]*\b{cls}\b[^"]*")>(.*?)</{tag}>' if cls else rf'<{tag}()>(.*?)</{tag}>')
        def f(m):
            got.append(m.group(2)); return f'<{tag} data-t {m.group(1)}>{m.group(2)}</{tag}>'.replace(" >", ">")
        b = re.sub(pat, f, b, flags=re.S)
    for tag, cls in [("h1", "cover__title"), ("h2", "chapter-title"), ("span", "chapter-label-text"), ("div", "fig__title"), ("div", "fig__what"),
                     ("span", "cover__date"), ("span", "cover__tag"), ("div", "q__tag"), ("div", "why__k"), ("p", "footer__text"), ("p", "footer__disclaimer"),
                     ("span", "sources__n"), ("span", "sources__k"), ("div", "kfig__k"), ("div", "kfig__l"), ("div", "kfig__s"), ("p", "excerpt-text"),
                     ("cite", None), ("figcaption", None)]:
        one(tag, cls)
    def pill(m): got.append(m.group(1)); return f'<div class="cover__pill"><span data-t>{m.group(1)}</span></div>'
    b = re.sub(r'<div class="cover__pill"><span>(.*?)</span></div>', pill, b, flags=re.S)
    def legend(m):
        def it(n): got.append(n.group(2)); return f'{n.group(1)}<em data-t>{n.group(2)}</em>{n.group(3)}'
        return re.sub(r'(</i>)([^<]+)(</span>)', it, m.group(0))
    b = re.sub(r'<div class="key-legend".*?</div>', legend, b, flags=re.S)
    b = re.sub(r'<div class="kfig__v">(.*?)</div>', lambda m: f'<div class="kfig__v" data-num="{m.group(1)}">{m.group(1)}</div>', b)
    return b, got
body_en = body
body, tagged = tag_page(body)
ui_missing += tagged
# Spanish for the docx blocks: the same bold-lead layout as the English bullets
def es_html(k):
    t = ES_P[k]
    if re.fullmatch(r"s2b\d", k):
        a, rest = t.split(": ", 1)
        return f"<b>{e(a + ':')}</b> {e(rest)}"
    return e(t)
ES_HTML = {}
for k in list(P["paras"]) + ["cover_sub"]:
    if k.startswith("src") or k.endswith("_h"): continue
    if k not in ES_P: ui_missing.append(f"[docx block] {k}")
    else: ES_HTML[k] = es_html(k)
ui_missing = [s for s in dict.fromkeys(ui_missing) if s not in ES_UI and s != "" and not re.fullmatch(r"[\d.,]+", s) and not s.startswith("[docx block]")] + [s for s in ui_missing if s.startswith("[docx block]")]
if ui_missing:
    open(f"{S}/es_missing.txt", "w", encoding="utf-8").write("\n".join(repr(s) for s in ui_missing))
    print(f"SPANISH MISSING: {len(ui_missing)} entries -> {S}/es_missing.txt"); sys.exit(1)
js = js.replace("/*__I18N__*/null", json.dumps({"p": ES_HTML, "ui": ES_UI}, ensure_ascii=False, separators=(",", ":")))

page = HEAD + css + "</style>\n</head>\n<body>\n\n" + body + \
    '\n<script src="deploy/d3.v7.min.js"></script>\n<script>\n' + js + "\n</script>\n\n</body></html>\n"
open(f"{PROJ}/index_93.html", "w", encoding="utf-8").write(page)
open(f"{PROJ}/index.html", "w", encoding="utf-8").write(page)   # GitHub Pages serves index.html at the site root

# ---- verification: every docx block used exactly once and unaltered (after EDITS); excerpts literal ----
fail = []
blocks = [k for k in P["paras"] if not k.startswith("src") and not k.endswith("_h")]
missing = [k for k in blocks if k not in used]
print("docx blocks:", len(blocks), "missing:", missing)
if missing: fail.append("missing blocks")
cnt = {k: len(re.findall(r'data-src="%s"' % k, body_en)) for k in blocks}
bad = {k: v for k, v in cnt.items() if v != 1}
print("data-src markers not exactly once:", bad)
if bad: fail.append("markers")
norm = lambda s: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
for k in blocks:
    seg = re.search(r'data-src="%s"[^>]*>(.*?)</(?:p|li)>' % k, body_en, flags=re.S)
    if not (seg and norm(seg.group(1)) == norm(e(paras[k]))):
        print("MISMATCH", k); fail.append("mismatch " + k)
fulln = norm(" ".join(paras[k] for k in blocks))
for ex in re.findall(r'class="[^"]*excerpt-text[^"]*">(.*?)</', body_en):
    ok = norm(ex) in fulln
    print("excerpt OK" if ok else "EXCERPT NOT IN DOCX", "|", norm(ex)[:70])
    if not ok: fail.append("excerpt")
# chapter titles read as the docx headings
for n in range(1, 9):
    h = P["paras"][f"s{n}_h"]
    m = re.search(r'chapter-num">0%d</span>.*?<h2 class="chapter-title">(.*?)</h2>' % n, body_en, flags=re.S)
    ok = bool(m) and norm(m.group(1)).replace(" ?", "?") == h.replace(" ?", "?")
    print(f"heading {n}:", "OK" if ok else f"DIFFERS | {norm(m.group(1)) if m else None!r} vs {h!r}")
    if not ok: fail.append(f"heading {n}")
assert "[EXT" not in page
print("sources listed:", len(srcs))
print(len(page), "bytes written")
if fail:
    print("BUILD CHECK FAILED:", fail); sys.exit(1)
