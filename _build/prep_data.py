"""Excel -> data.json for In Depth #92. Columns are read by header name, never by position.
Usage: python -X utf8 _build/prep_data.py DATA/Charging_vs_Fuel_InDepth_Data.xlsx _build/data.json
ND ("no defensible figure") becomes null and is never treated as zero."""
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

def num(v, nd=(None,)):
    return None if v in nd else (round(v, 4) if isinstance(v, float) else v)

# ISO-3 -> ISO numeric (ids used by world-atlas countries-110m). Singapore is too small for 110m.
ISO_NUM = {"CHN": "156", "USA": "840", "DEU": "276", "GBR": "826", "FRA": "250", "NLD": "528", "NOR": "578",
           "CAN": "124", "KOR": "410", "SWE": "752", "BEL": "056", "JPN": "392", "ITA": "380", "DNK": "208",
           "ESP": "724", "AUS": "036", "TUR": "792", "IND": "356", "CHE": "756", "BRA": "076", "THA": "764",
           "AUT": "040", "FIN": "246", "PRT": "620", "ISR": "376", "VNM": "704", "POL": "616", "ARE": "784",
           "IDN": "360", "MEX": "484", "NZL": "554", "MYS": "458", "ISL": "352", "GRC": "300", "SGP": "702",
           "COL": "170", "PHL": "608", "CRI": "188", "CHL": "152", "ZAF": "710"}

ISO2 = {"CHN": "cn", "USA": "us", "DEU": "de", "GBR": "gb", "FRA": "fr", "NLD": "nl", "NOR": "no", "CAN": "ca",
        "KOR": "kr", "SWE": "se", "BEL": "be", "JPN": "jp", "ITA": "it", "DNK": "dk", "ESP": "es", "AUS": "au",
        "TUR": "tr", "IND": "in", "CHE": "ch", "BRA": "br", "THA": "th", "AUT": "at", "FIN": "fi", "PRT": "pt",
        "ISR": "blank", "VNM": "vn", "POL": "pl", "ARE": "ae", "IDN": "id", "MEX": "mx", "NZL": "nz", "MYS": "my",
        "ISL": "is", "GRC": "gr", "SGP": "sg", "COL": "co", "PHL": "ph", "CRI": "cr", "CHL": "cl", "ZAF": "za"}

D = {}

pts = rows("03_Charging_Points", 1)
D["points"] = [{"m": r["Market"], "region": r["Region"], "total": r["Public points, end-2025 (IEA)"],
                "fast": r["of which fast + ultra-fast (>22 kW)"], "slow": r["Slow (<=22 kW)"],
                "share": num(r["Fast share"])} for r in pts if r["Public points, end-2025 (IEA)"] is not None]
D["points_nd"] = [r["Market"] for r in pts if r["Public points, end-2025 (IEA)"] is None]
for r in D["points"]:
    if r["fast"] is not None: assert r["fast"] + r["slow"] == r["total"], r

cs = {r["Slice"]: r for r in rows("04_China_Share", 1)}
D["china"] = {"china": cs["China"]["Public points, end-2025"], "rest": cs["Rest of the world"]["Public points, end-2025"],
              "world": cs["World (sum of IEA country table)"]["Public points, end-2025"], "share": num(cs["China"]["Share"])}
assert D["china"]["china"] + D["china"]["rest"] == D["china"]["world"]

st = rows("05_Fuel_Stations", 1)
D["stations"] = [{"m": r["Market"], "region": r["Region"], "n": r["Fuel stations"], "date": r["Reference date"],
                  "grade": r["Grade"], "note": r["Note"]} for r in st if r["Fuel stations"] is not None]
D["stations_nd"] = [r["Market"] for r in st if r["Fuel stations"] is None]

fl = rows("06_Fleets", 1)
D["fleets"] = [{"m": r["Market"], "scope": r["Fleet scope"], "date": r["Reference date"], "total": r["Total fleet"],
                "bev": r["BEV"], "phev": r["PHEV"], "ev": r["EV (BEV+PHEV)"], "ice": r["Combustion (total - EV)"],
                "share": num(r["EV share of fleet"]), "grade": r["Grade"], "note": r["Note"]}
               for r in fl if r["Total fleet"] is not None]
D["fleets_nd"] = [r["Market"] for r in fl if r["Total fleet"] is None]
for r in D["fleets"]: assert r["ev"] + r["ice"] == r["total"], r["m"]

ra = rows("07_Ratios", 1)
D["ratios"] = [{"m": r["Market"], "evpp": num(r["EVs per public point (IEA cars, end-2025 / IEA points, end-2025)"]),
                "icepst": num(r["Combustion vehicles per fuel station"]), "fdate": r["Fleet date"], "sdate": r["Stations date"]}
               for r in ra]

pp = rows("08_Points_per_Station", 1)
D["pps"] = [{"m": r["Market"], "v": num(r["Public charging points per fuel station"]), "points": r["Public points (end-2025)"],
             "stations": r["Fuel stations"], "sdate": r["Stations date"]} for r in pp]

mp = rows("09_Map", 1)
D["map"] = [{"iso3": r["ISO-3"], "id": ISO_NUM[r["ISO-3"]], "m": r["Market"], "v": num(r["Public points per fuel station"])} for r in mp]
assert len(D["map"]) == 40

sc = rows("10_Scatter", 0)
D["scatter"] = [{"m": r["Market"], "x": num(r["EV share of fleet (x)"]), "y": num(r["EVs per public point (y)"]),
                 "date": r["Fleet date"], "region": r["Region"]} for r in sc]

# cross-checks between sheets
by = lambda L: {d["m"]: d for d in L}
P, S = by(D["points"]), by(D["stations"])
for d in D["pps"]:
    assert P[d["m"]]["total"] == d["points"] and S[d["m"]]["n"] == d["stations"], d["m"]
    assert abs(d["points"] / d["stations"] - d["v"]) < 1e-3, d["m"]
M = {d["m"]: d["v"] for d in D["map"]}
for d in D["pps"]: assert abs(M[d["m"]] - d["v"]) < 1e-3, d["m"]

# flag code per market name (deploy/flags/<code>.svg, flag-icons 1x1)
D["flags"] = {d["m"]: ISO2[d["iso3"]] for d in D["map"]}
D["flags"]["Israel"] = "blank"   # editorial choice: Israel is shown with a plain white tile, not its flag
for k in ("points", "stations", "fleets", "ratios", "pps", "scatter"):
    for d in D[k]: assert d["m"] in D["flags"], (k, d["m"])

json.dump(D, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
for k, v in D.items(): print(f"{k:12s}", len(v) if isinstance(v, list) else v)
