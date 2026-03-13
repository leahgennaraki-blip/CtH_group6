import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "Data_Set_S1.txt"
TABLES = ROOT / "tables"
TABLES.mkdir(exist_ok=True)

# ---------- Load labMT safely ----------
with open(DATA, "r", encoding="utf-8") as f:
    lines = f.readlines()

header_index = None
for i, line in enumerate(lines):
    if line.lower().startswith("word\t"):
        header_index = i
        break

df = pd.read_csv(DATA, sep="\t", skiprows=header_index, na_values=["--"])
df.columns = [c.strip() for c in df.columns]

# numeric columns
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------- Base categories ----------
pos5 = df.sort_values("happiness_average", ascending=False).head(5).copy()
pos5["category"] = "very positive"

neg5 = df.sort_values("happiness_average", ascending=True).head(5).copy()
neg5["category"] = "very negative"

con5 = df.sort_values("happiness_standard_deviation", ascending=False).head(5).copy()
con5["category"] = "highly contested"

# ---------- NEW: polarization category ----------
# Near-neutral average but high disagreement
polar5 = (
    df[df["happiness_average"].between(4.5, 5.5)]
    .sort_values("happiness_standard_deviation", ascending=False)
    .head(5)
    .copy()
)
polar5["category"] = "polarizing (neutral avg, high disagreement)"

exhibit_cols = [
    "category",
    "word",
    "happiness_average",
    "happiness_standard_deviation",
    "twitter_rank",
    "google_rank",
    "nyt_rank",
    "lyrics_rank",
]

exhibit = pd.concat([pos5, neg5, con5, polar5], ignore_index=True)[exhibit_cols]

out_path = TABLES / "word_exhibit_20_words_polarization.csv"
exhibit.to_csv(out_path, index=False)

print("Saved:", out_path)
print(exhibit.to_string(index=False))