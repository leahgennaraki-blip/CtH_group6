from pathlib import Path

import pandas as pd


def main():
    # Use the multi-page processed dataset as the main corpus
    processed_path = Path("data/processed/guardian_articles_pages1_3.csv")

    if not processed_path.exists():
        raise FileNotFoundError(
            f"{processed_path} not found. "
            f"Please run 'python src/process_guardian_multi.py' first."
        )

    df = pd.read_csv(processed_path)

    print("Loaded DataFrame shape:", df.shape)
    print("Columns:", list(df.columns))

    # Quick look at the first few rows
    print("\n=== Head of the DataFrame ===")
    print(df.head(5))

    # Count how many articles per section_name
    section_counts = (
        df["section_name"]
        .fillna("UNKNOWN")
        .value_counts()
        .rename_axis("section_name")
        .reset_index(name="article_count")
    )

    print("\n=== Article counts by section_name ===")
    print(section_counts)

    # Save this summary to tables/
    tables_dir = Path("tables")
    tables_dir.mkdir(parents=True, exist_ok=True)

    output_path = tables_dir / "guardian_section_counts_pages1_3.csv"
    section_counts.to_csv(output_path, index=False)

    print(f"\nSaved section counts table to: {output_path.resolve()}")


if __name__ == "__main__":
    main()