"""Excel -> data93.json for In Depth #93. Columns are read by header name, never by position.
Usage: python -X utf8 _build/prep_data93.py DATA/Most_Efficient_Mover_InDepth_Data.xlsx _build/data93.json
ND ("no defensible figure") becomes null and is never treated as zero. Nothing is estimated."""
import json, sys, openpyxl

xl, out = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(xl, data_only=True)

def rows(sheet, header_row):
    """Rows of a sheet as dicts keyed by the header found on `header_row` (0-based)."""
    allr = list(wb[sheet].iter_rows(values_only=True))
    head = [h.strip() if isinstance(h, str) else h for h in allr[header_row]]
    o = []
    for r in allr[header_row + 1:]:
        if r[0] is None: continue
        o.append({h: (None if v == "ND" else v) for h, v in zip(head, r) if h})
    return o

def mover(r, extra=()):
    """The columns every mover sheet shares."""
    d = {"id": r["ID"], "mover": r["Mover"], "detail": r.get("Detail"), "basis": r["Basis"],
         "boundary": r["Energy boundary"], "low": r["COT low"], "cot": r["COT central"], "high": r["COT high"],
         "grade": r["Grade"], "note": r.get("Note")}
    if "Group" in r: d["group"] = r["Group"]
    if "Inputs and conversion" in r: d["inputs"] = r["Inputs and conversion"]
    for k, h in extra: d[k] = r[h]
    return d

G, KG_PERSON = 9.80665, 75
WH_PKM = KG_PERSON * G / 3.6      # Wh per person-km per unit of COT (75 kg passenger)
WH_TKM = 1000 * G / 3.6           # Wh per tonne-km per unit of COT

D = {}

D["champions"] = [{"cls": r["Class"], "mover": r["Champion"], "detail": r["Detail"], "cot": r["COT"], "basis": r["Basis"],
                   "boundary": r["Boundary"], "grade": r["Grade"]} for r in rows("02_Champions", 0)]
assert len(D["champions"]) == 6

ladder = [mover(r) for r in rows("03_COT_Ladder", 1)]
D["ladder"] = sorted((d for d in ladder if d["cot"] is not None), key=lambda d: d["cot"])
D["ladder_nd"] = [d["mover"] for d in ladder if d["cot"] is None]
assert [d["id"] for d in D["ladder"]][0] == "L01" and D["ladder"][-1]["id"] == "F07"
for d in D["ladder"]: assert d["low"] <= d["cot"] <= d["high"], d["id"]

D["size"] = [{"kg": r["Body mass (kg)"], "cot": r["Net COT, running (model)"], "label": r["Label"]}
             for r in rows("04_Size_Matters", 1)]
byl = {d["label"]: d for d in D["size"] if d["label"]}
D["size_ratio"] = byl["Mouse"]["cot"] / byl["Elephant"]["cot"]
assert round(D["size_ratio"]) == 47

D["living"] = [mover(r) for r in rows("05_Living_Beings", 0)]
D["human"] = [mover(r, (("practical", "Practical value"),)) for r in rows("06_Human_Body", 0)]
D["robots"] = [mover(r) for r in rows("07_Robots", 0)]

ppl = [mover(r, (("wh", "Wh per person-km"),)) for r in rows("08_Moving_People", 1)]
for d in ppl:                       # the Wh column and the COT column must tell the same story
    assert abs(d["cot"] * WH_PKM - d["wh"]) / d["wh"] < 0.01, d["id"]
    d["wh_low"], d["wh_high"] = d["low"] * WH_PKM, d["high"] * WH_PKM
# the Excel note for the double-decker gives the occupancy range (20 to 80 on board): 22-89 Wh per person-km
bus = next(d for d in ppl if d["id"] == "V05"); assert "22-89" in bus["note"]
bus["wh_low"], bus["wh_high"] = 22, 89
D["people"] = sorted(ppl, key=lambda d: d["wh"])

gds = [mover(r, (("wh", "Wh per tonne-km"),)) for r in rows("09_Moving_Goods", 1)]
for d in gds:
    if d["wh"] is not None:
        assert abs(d["cot"] * WH_TKM - d["wh"]) / d["wh"] < 0.01, d["id"]
        d["wh_low"], d["wh_high"] = d["low"] * WH_TKM, d["high"] * WH_TKM
D["goods"] = sorted((d for d in gds if d["wh"] is not None), key=lambda d: d["wh"])
D["goods_whole"] = [d for d in gds if d["wh"] is None]       # F04: whole truck, no tonne-km figure
assert [d["id"] for d in D["goods_whole"]] == ["F04"]

F = {r["Constant or formula"]: r for r in rows("10_Formula", 0)}
D["formula"] = {"g": F["g"]["Value"], "passenger_kg": F["Mass per passenger"]["Value"]}
assert D["formula"] == {"g": G, "passenger_kg": KG_PERSON}

# cross-checks: a mover that appears on several sheets carries the same COT everywhere
L = {d["mover"]: d for d in D["ladder"]}
for sheet in ("living", "human", "robots", "people", "goods"):
    for d in D[sheet] if sheet != "goods" else D["goods"] + D["goods_whole"]:
        if d["cot"] is None: continue
        name = d["mover"].replace(" (reference)", "")
        if name in L: assert abs(L[name]["cot"] - d["cot"]) < 1e-9, (sheet, name)
assert abs(L["Humpback whale"]["cot"] - D["champions"][0]["cot"]) < 1e-9

json.dump(D, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
for k, v in D.items(): print(f"{k:12s}", len(v) if isinstance(v, (list, dict)) else v)
print("ladder ND:", D["ladder_nd"])
