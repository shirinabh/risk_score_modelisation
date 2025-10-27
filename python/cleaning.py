# cleaning.py
import csv, re
import pandas as pd

inp = "Webstat_Export_fr_entreprises_defaillances-entreprises.csv"
sep = ';'

def detect_encoding(path, n=65536):
    with open(path, 'rb') as fb:
        raw = fb.read(n)
    for enc in ("utf-8-sig", "utf-8", "cp1252", "iso-8859-1"):
        try:
            raw.decode(enc)
            return enc
        except UnicodeDecodeError:
            pass
    return "iso-8859-1"

enc_in = detect_encoding(inp)

# ---- L1 titres, L2 codes ----
with open(inp, 'r', encoding=enc_in, newline="") as f:
    r = csv.reader(f, delimiter=sep)
    titles = next(r)[1:]
    codes  = next(r)[1:]

n = min(len(titles), len(codes))
titles = [x.strip() for x in titles[:n]]
codes  = [x.strip() for x in codes[:n]]

# ---- normalisation + dédup pour BQ ----
seen, bq = {}, []
for raw in (c := [x.replace('.', '_') for x in codes]):
    if raw in seen:
        seen[raw] += 1
        bq.append(f"{raw}__{seen[raw]}")
    else:
        seen[raw] = 0
        bq.append(raw)

# ---- helpers d'extraction ----
def parse_region(s: str) -> str | None:
    return s.split(" - ", 1)[0].strip() if " - " in s else None

_period_re = re.compile(r"(?:sur|le)\s+((?:\d+\s*mois)|(?:le\s+mois)|(?:trimestre))", re.IGNORECASE)

def parse_period(s: str) -> str | None:
    m = _period_re.search(s)
    if not m:
        return None
    p = m.group(1).strip().lower()
    return p.replace("le ", "")  # "le mois" -> "mois"

def parse_sector(s: str) -> str | None:
    parts = [p.strip() for p in s.split(" - ")]
    return parts[2] if len(parts) >= 3 else None

# ---- codes.csv ----
codes_df = pd.DataFrame({
    "business_failure_code_bq": bq,
    "business_failure_code": codes,
    "business_failure_description": titles
})

codes_df["region_name"]  = codes_df["business_failure_description"].apply(parse_region)
codes_df["period_scope"] = codes_df["business_failure_description"].apply(parse_period)   # "12 mois" | "trimestre" | "mois"
codes_df["sector_name"]  = codes_df["business_failure_description"].apply(parse_sector)   # ex: "Information et communication"

# ordre demandé: code_bq, region, period_scope, sector_name, code, description
codes_df = codes_df[[
    "business_failure_code_bq",      # index 0
    "region_name",                   # index 1
    "period_scope",                  # index 2
    "sector_name",                   # index 3
    "business_failure_code",         # index 4
    "business_failure_description"   # index 5
]]

codes_df.to_csv("codes.csv", index=False, sep=sep, encoding="utf-8-sig")

# ---- données: on supprime lignes 0..5 (donc 1 à 6) ----
df = pd.read_csv(inp, sep=sep, encoding=enc_in, skiprows=[0,1,2,3,4,5], header=None)
m = df.shape[1]
hdr = bq

if m == len(hdr) + 1:
    cols = ["date"] + hdr
elif m == len(hdr):
    cols = hdr
elif m > len(hdr) + 1:
    cols = ["date"] + hdr + [f"extra_{i}" for i in range(m - len(hdr) - 1)]
else:
    cols = (["date"] + hdr)[:m]

df.columns = cols
df.to_csv("nettoyage_defaillances.csv", index=False, sep=sep, encoding="utf-8-sig")
print(f"encoding source: {enc_in}")
