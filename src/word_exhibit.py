import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "Data_Set_S1.txt"
TABLES = ROOT / "tables"
TABLES.mkdir(exist_ok=True)

# -------- LOAD DATA CORRECTLY --------
with open(DATA, "r", encoding="utf-8") as f:
    lines = f.readlines()

header_index = None
for i, line in enumerate(lines):
    if line.lower().startswith("word\t"):
        header_index = i
        break

df = pd.read_csv(DATA, sep="\t", skiprows=header_index, na_values="--")
df.columns = [c.strip() for c in df.columns]

# Convert numeric columns
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -------- BUILD CATEGORIES --------

# 5 very positive
pos5 = df.sort_values("happiness_average", ascending=False).head(5).copy()
pos5["category"] = "very positive"

# 5 very negative
neg5 = df.sort_values("happiness_average", ascending=True).head(5).copy()
neg5["category"] = "very negative"

# 5 highly contested
con5 = df.sort_values("happiness_standard_deviation", ascending=False).head(5).copy()
con5["category"] = "highly contested"

# 5 platform-specific (Twitter-common, NYT-missing)
platform5 = (
    df[df["twitter_rank"].notna() & df["nyt_rank"].isna()]
    .sort_values("twitter_rank")
    .head(5)
    .copy()
)
platform5["category"] = "platform-specific (Twitter-common, NYT-missing)"

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

exhibit = pd.concat([pos5, neg5, con5, platform5], ignore_index=True)[exhibit_cols]

# Save
out_path = TABLES / "word_exhibit_20_words.csv"
exhibit.to_csv(out_path, index=False)

print("Saved:", out_path)
print(exhibit.to_string(index=False))