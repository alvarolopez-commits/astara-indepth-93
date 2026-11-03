"""Extract the editorial blocks of the #93 docx verbatim, keyed by section/paragraph.
Usage: python -X utf8 _build/docx_paras93.py DATA/Most_Efficient_Mover_InDepth_Content.docx _build/paras93.json

Keys: how1..4 (reading rules), sum1..3 (thesis), s<N>p<k> (paragraphs), s<N>b<k> (bullets), src<k> (Appendix B).
Not published as reader text and kept apart: the cover strapline ("FORTNIGHTLY IN-DEPTH · BASE CONTENT FOR DESIGN"),
the designer's opening note under "How to read this document", the visual notes ("VISUAL Vxx" + "Data: ..."),
the data tables, Appendix A (visual list) and Appendix C (limits)."""
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

paras, tables, visuals, appendix, notes = {}, [], [], {"A": [], "C": []}, []
cover = []          # the unstyled paragraphs between the title and the first heading: subtitle, "Prepared ..." line
sec = None          # "how", "sum", "s1".."s8", "appA", "appB", "appC", or None (cover)
counters = {}
title = None
last_visual = None

for child in body:
    if child.tag == W + "tbl":
        rows = []
        for tr in child.findall(W + "tr"):
            rows.append([" ".join(t for t in (ptext(p) for p in tc.iter(W + "p")) if t) for tc in tr.findall(W + "tc")])
        if sec == "appA": appendix["A"] = rows; continue
        tables.append({"section": sec, "rows": rows})
        continue
    if child.tag != W + "p": continue
    t, st = ptext(child), pstyle(child)
    if not t: continue
    if st == "Title": title = t; continue
    if st == "Heading1":
        if t == "How to read this document": sec = "how"
        elif t == "The thesis in one page": sec = "sum"
        elif t.startswith("Appendix A"): sec = "appA"
        elif t.startswith("Appendix B"): sec = "appB"
        elif t.startswith("Appendix C"): sec = "appC"
        else:
            m = re.match(r"(\d+)\. (.*)", t); assert m, t
            sec = "s" + m.group(1); paras[sec + "_h"] = m.group(2)
        continue
    if st == "Heading2": continue   # "Key figures" (rendered as V01)
    if sec is None:
        if t.startswith("FORTNIGHTLY IN-DEPTH"): continue
        cover.append(t); continue
    if t.startswith("VISUAL V"):
        last_visual = {"label": t, "note": "", "section": sec}; visuals.append(last_visual); continue
    if t.startswith("Data: ") and last_visual is not None and not last_visual["note"]:
        last_visual["note"] = t; continue
    if sec == "appC": appendix["C"].append(t); continue
    if sec == "appA": continue
    if sec == "appB":
        counters["src"] = counters.get("src", 0) + 1; paras[f"src{counters['src']}"] = t; continue
    kind = "b" if st.startswith("List") else "p"
    if sec in ("how", "sum"): kind = ""
    if sec == "how" and kind == "" and not st.startswith("List"):
        notes.append(t); continue   # designer's opening note
    key = sec + kind
    counters[key] = counters.get(key, 0) + 1
    paras[f"{key}{counters[key]}"] = t

# the "how" bullets are listed as how1..4, the thesis paragraphs as sum1..3
paras = {re.sub(r"^how(\d)", r"how\1", k): v for k, v in paras.items()}
json.dump({"title": title, "cover": cover, "paras": paras, "tables": tables, "visuals": visuals, "appendix": appendix, "notes": notes},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("title:", title)
print("cover:", cover)
print("blocks:", {k: sum(1 for p in paras if re.fullmatch(k + r"\d+", p)) for k in
      ["how", "sum", "s1p", "s2p", "s2b", "s3p", "s4p", "s5p", "s6p", "s7b", "s8b", "src"]})
print("tables:", [(t["section"], len(t["rows"])) for t in tables])
print("visuals:", [v["label"][:14] for v in visuals])
