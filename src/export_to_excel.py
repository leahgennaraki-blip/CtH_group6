import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "Data_Set_S1.txt"
OUT = ROOT / "tables"
OUT.mkdir(exist_ok=True)

# Find header row
with open(DATA, "r", encoding="utf-8") as f:
    lines = f.readlines()

header_index = None
for i, line in enumerate(lines):
    if line.lower().startswith("word\t"):
        header_index = i
        break

df = pd.read_csv(DATA, sep="\t", skiprows=header_index, na_values="--")

# Convert numeric columns
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Export to Excel
excel_path = OUT / "labmt_full_dataset.xlsx"
df.to_excel(excel_path, index=False)

print("Saved:", excel_path)