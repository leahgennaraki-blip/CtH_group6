from __future__ import annotations
import pandas as pd
from pathlib import Path

RAW_PATH = Path("/Users/tianyesmacbookpro16/Documents/UvA/Coding the Humanities/Hedonometer/hedonometer-project/data/raw/Data_Set_S1.txt")  # <-- rename to your actual filename

def load_labmt(path: Path = RAW_PATH) -> pd.DataFrame:
    """
    Load labMT 1.0 tab-delimited file.

    Assumptions from assignment:
    - File may contain metadata/comment lines before the header.
    - Missing ranks are represented as '--'.
    """
    # Read whole file to find the header line robustly
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    # Heuristic: header line contains 'word' and 'happiness' (adjust if needed)
    header_idx = None
    for i, line in enumerate(lines[:200]):  # header is near the top
        if "\t" in line and "word" in line.lower() and "happiness" in line.lower():
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Could not find header row. Inspect the raw file and adjust header detection.")

    # Now read using pandas starting at the header row
    df = pd.read_csv(
        path,
        sep="\t",
        skiprows=header_idx,
        na_values=["--"],
        keep_default_na=True,
        dtype=str,  # load as str first; we’ll coerce numeric
    )

    # Strip whitespace in column names
    df.columns = [c.strip() for c in df.columns]

    # Typical numeric columns in labMT
    numeric_cols = [c for c in df.columns if c != "word"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Basic cleanup
    df["word"] = df["word"].astype(str).str.strip()

    return df

def main() -> None:
    df = load_labmt()
    print("Shape (rows, cols):", df.shape)
    print("\nColumns:", list(df.columns))
    print("\nMissing values per column:\n", df.isna().sum().sort_values(ascending=False))
    print("\nDuplicate words:", df["word"].duplicated().sum())
    print("\nSample rows:\n", df.sample(15, random_state=42))

if __name__ == "__main__":
    main()