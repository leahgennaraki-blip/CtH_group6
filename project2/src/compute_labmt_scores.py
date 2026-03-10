from pathlib import Path
import re

import pandas as pd

from load_labmt import load_labmt


def build_labmt_lexicon() -> dict[str, float]:
    """
    Load the LabMT data using load_labmt() and return a dictionary
    mapping word -> happiness score (happiness_average).
    """
    labmt_df = load_labmt()

    # We assume the columns are called 'word' and 'happiness_average'
    if "word" not in labmt_df.columns or "happiness_average" not in labmt_df.columns:
        raise KeyError(
            "Expected columns 'word' and 'happiness_average' in LabMT data. "
            f"Found columns: {list(labmt_df.columns)}"
        )

    # Drop any rows where the score is missing
    labmt_df = labmt_df.dropna(subset=["happiness_average"])

    lexicon = dict(zip(labmt_df["word"].astype(str), labmt_df["happiness_average"]))
    print(f"Built LabMT lexicon with {len(lexicon)} words.")
    return lexicon


def tokenize(text: str) -> list[str]:
    """
    Very simple tokenizer:
    - lower-case the text
    - keep only alphabetic characters and apostrophes
    - return a list of tokens
    """
    if not isinstance(text, str):
        return []

    tokens = re.findall(r"[a-zA-Z']+", text.lower())
    return tokens


def compute_happiness_score(
    text: str,
    lexicon: dict[str, float],
    min_matches: int = 5,
) -> tuple[float | None, int, int]:
    """
    Compute the average happiness score for a piece of text.

    Returns a tuple:
    (happiness_score or None, matched_token_count, total_token_count)
    """
    tokens = tokenize(text)
    total_tokens = len(tokens)

    scores = [lexicon[token] for token in tokens if token in lexicon]
    matched_tokens = len(scores)

    if matched_tokens < min_matches:
        # Not enough matched words to make a reliable score
        return None, matched_tokens, total_tokens

    happiness_score = float(sum(scores) / matched_tokens)
    return happiness_score, matched_tokens, total_tokens


def main():
    # 1. Build LabMT lexicon (word -> score)
    lexicon = build_labmt_lexicon()

    # 2. Load the processed Guardian articles (multi-page corpus)
    articles_path = Path("data/processed/guardian_articles_pages1_3.csv")

    if not articles_path.exists():
        raise FileNotFoundError(
            f"{articles_path} not found. "
            f"Please run 'python src/process_guardian_multi.py' first."
        )

    df = pd.read_csv(articles_path)
    print("Loaded articles DataFrame shape:", df.shape)

    if "body_text" not in df.columns:
        raise KeyError(
            "Expected a 'body_text' column in the Guardian articles CSV. "
            f"Found columns: {list(df.columns)}"
        )

    # 3. Compute happiness scores for each article
    print("\nComputing happiness scores for each article...")
    results = df["body_text"].apply(
        lambda text: compute_happiness_score(text, lexicon, min_matches=5)
    )

    # Split the tuple into three separate columns
    df["happiness_score"] = results.apply(lambda t: t[0])
    df["matched_token_count"] = results.apply(lambda t: t[1])
    df["total_token_count"] = results.apply(lambda t: t[2])

    print("\n=== Example rows with happiness scores ===")
    print(
        df[
            [
                "section_name",
                "web_title",
                "happiness_score",
                "matched_token_count",
                "total_token_count",
            ]
        ].head(10)
    )

    # 4. Save the scored dataset
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    output_path = processed_dir / "guardian_articles_pages1_3_with_scores.csv"
    df.to_csv(output_path, index=False)

    print(f"\nSaved scored dataset to: {output_path.resolve()}")


if __name__ == "__main__":
    main()