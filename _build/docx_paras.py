"""Extract the editorial blocks of the #92 docx verbatim, keyed by section/paragraph.
Usage: python -X utf8 _build/docx_paras.py DATA/Charging_vs_Fuel_InDepth_Content.docx _build/paras.json

Keys: sum1..3 (summary), s<N>p<k> (paragraphs), s<N>b<k> (bullets), src<k> (Appendix B).
Visual notes ("VISUAL Vxx" + "Data: ...") and the data tables are design instructions, not
reader text: they are recorded under "visuals" and "tables" but never published as paragraphs.
Appendix A (visual list) and Appendix C (limits) are kept under "appendix" for reference."""
import json, re, sys, zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
src, out = sys.argv[1], sys.argv[2]
root = ET.fromstring(zipfile.ZipFile(src).read("word/document.xml"))
body = root.find(W + "body")

def ptext(p):
    o = []
    for el in p.iter():
        if el.tag == W + "t": o.append(el.text or "")
        elif el.tag == W + "tab": o.append("\t")
        elif el.tag == W + "br": o.append("\n")
    return "".join(o).strip()

def pstyle(p):
    s = p.find(f"{W}pPr/{W}pStyle")
    return s.get(W + "val") if s is not None else ""

paras, tables, visuals, appendix, fulltext = {}, [], [], {"A": [], "C": []}, []
sec = None          # "sum", "s1".."s7", "appA", "appB", "appC", or None (cover)
counters = {}
title = None
last_visual = None

for child in body:
    if child.tag == W + "tbl":
        rows = []
        for tr in child.findall(W + "tr"):
            rows.append([" ".join(t for t in (ptext(p) for p in tc.iter(W + "p")) if t) for tc in tr.findall(W + "tc")])
        if sec in ("appA",): appendix["A"] = rows; continue
        tables.append({"section": sec, "rows": rows})
        continue
    if child.tag != W + "p": continue
    t, st = ptext(child), pstyle(child)
    if not t: continue
    if st == "Title": title = t; continue
    if st == "Heading1":
        if t == "Summary": sec = "sum"
        elif t.startswith("Appendix A"): sec = "appA"
        elif t.startswith("Appendix B"): sec = "appB"
        elif t.startswith("Appendix C"): sec = "appC"
        else:
            m = re.match(r"(\d+)\. (.*)", t); assert m, t
            sec = "s" + m.group(1); paras[sec + "_h"] = m.group(2)
        continue
    if st == "Heading2": continue   # "Key figures" (rendered as V01)
    if sec is None: continue        # "FORTNIGHTLY IN-DEPTH · BASE CONTENT FOR DESIGN"
    if t.startswith("VISUAL V"):
        last_visual = {"label": t, "note": "", "section": sec}; visuals.append(last_visual); continue
    if t.startswith("Data: ") and last_visual is not None and not last_visual["note"]:
        last_visual["note"] = t; continue
    if sec == "appC": appendix["C"].append(t); continue
    if sec == "appA": continue
    if sec == "appB":
        counters["src"] = counters.get("src", 0) + 1; paras[f"src{counters['src']}"] = t; continue
    fulltext.append(t)
    kind = "b" if st.startswith("List") else "p"
    if sec == "sum": kind = ""
    key = sec + kind
    counters[key] = counters.get(key, 0) + 1
    paras[f"{key}{counters[key]}"] = t

json.dump({"title": title, "paras": paras, "tables": tables, "visuals": visuals, "appendix": appendix,
           "fulltext": " ".join(fulltext)}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in paras.items():
    print(f"{k:7s} {len(v):4d} | {v[:70]}")
print(len(tables), "tables;", len(visuals), "visual notes;", len(appendix["C"]), "limits")
