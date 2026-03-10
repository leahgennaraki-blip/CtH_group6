from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_scored_articles() -> pd.DataFrame:
    """Load the Guardian articles with happiness scores."""
    path = Path("data/processed/guardian_articles_pages1_3_with_scores.csv")
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run 'python src/compute_labmt_scores.py' first."
        )

    df = pd.read_csv(path)
    print("Loaded scored DataFrame shape:", df.shape)
    print("Columns:", list(df.columns))

    # Keep only rows with a valid happiness_score
    df = df.dropna(subset=["happiness_score"])
    print("After dropping NaN happiness_score:", df.shape)

    return df


def plot_overall_distribution(df: pd.DataFrame, output_dir: Path) -> None:
    """Plot overall distribution of happiness_score."""
    plt.figure(figsize=(8, 5))
    sns.histplot(df["happiness_score"], bins=30, kde=True, color="steelblue")

    plt.title("Distribution of article happiness scores")
    plt.xlabel("Happiness score (LabMT average per article)")
    plt.ylabel("Number of articles")

    output_path = output_dir / "happiness_distribution_overall.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved overall distribution figure to: {output_path.resolve()}")


def plot_by_section(df: pd.DataFrame, output_dir: Path, min_articles: int = 10) -> None:
    """
    Plot happiness_score by section_name for sections with at least min_articles.
    Uses a boxplot to compare distributions.
    """
    # Count articles per section
    counts = df["section_name"].value_counts()
    print("\nArticle counts per section_name (scored rows):")
    print(counts)

    # Keep only sections with enough articles
    valid_sections = counts[counts >= min_articles].index.tolist()
    print(f"\nSections with at least {min_articles} articles:", valid_sections)

    df_subset = df[df["section_name"].isin(valid_sections)].copy()

    if df_subset.empty:
        print("No sections with enough articles to plot.")
        return

    plt.figure(figsize=(10, 6))
    sns.boxplot(
        data=df_subset,
        x="section_name",
        y="happiness_score",
        order=valid_sections,
    )

    plt.title("Article happiness scores by section (>= "
              f"{min_articles} articles per section)")
    plt.xlabel("Section name")
    plt.ylabel("Happiness score (LabMT)")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = output_dir / "happiness_by_section_boxplot.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved by-section boxplot to: {output_path.resolve()}")


def main():
    df = load_scored_articles()

    figures_dir = Path("figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Overall happiness distribution
    plot_overall_distribution(df, figures_dir)

    # 2. Happiness distribution by section
    plot_by_section(df, figures_dir, min_articles=10)


if __name__ == "__main__":
    main()