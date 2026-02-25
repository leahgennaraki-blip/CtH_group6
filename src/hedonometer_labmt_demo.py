from __future__ import annotations

from pathlib import Path
import pandas as pd

# === 路径设置：根据当前脚本的位置，自动找到项目根目录 ===
# 当前文件在 hedonometer-project-group6/src/load_labmt.py
# parents[0] -> src
# parents[1] -> hedonometer-project-group6  (项目根目录)
BASE_DIR = Path(__file__).resolve().parents[1]

# 数据文件就在 项目根目录/data/raw/Data_Set_S1.txt
RAW_PATH = BASE_DIR / "data" / "raw" / "Data_Set_S1.txt"


def load_labmt(path: Path = RAW_PATH) -> pd.DataFrame:
    """
    Load labMT 1.0 tab-delimited file.

    Assumptions from assignment:
    - File may contain metadata/comment lines before the header.
    - Missing ranks are represented as '--'.
    """


    # 读取整个文件，找到真正的表头行
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    # 启发式：表头那一行里既有 'word' 又有 'happiness'
    header_idx: int | None = None
    for i, line in enumerate(lines[:200]):  # header 应该在文件前 200 行之内
        if "\t" in line and "word" in line.lower() and "happiness" in line.lower():
            header_idx = i
            break

    if header_idx is None:
        raise ValueError(
            "Could not find header row. Inspect the raw file and adjust header detection."
        )

    # 从表头开始，用 pandas 读入
    df = pd.read_csv(
        path,
        sep="\t",
        skiprows=header_idx,
        na_values=["--"],        # 把 '--' 当作缺失值
        keep_default_na=True,
        dtype=str,               # 先按字符串读，后面再转数值
    )

    # 去掉列名两端的空格
    df.columns = [c.strip() for c in df.columns]

    # 除了 'word' 以外的列都尝试转成数值
    numeric_cols = [c for c in df.columns if c != "word"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # 处理 word 列：转成字符串并去掉空格
    df["word"] = df["word"].astype(str).str.strip()

    return df


def main() -> None:
    df = load_labmt()

    # === 1.1 + 1.2 + 1.3 所有需要的输出 ===

    # 1) 形状（行 × 列）
    print("Shape (rows, cols):", df.shape)

    # 2) 列名列表
    print("\nColumns:", list(df.columns))

    # 3) 每一列的数据类型（data dictionary 用）
    print("\nData types:\n", df.dtypes)

    # 4) 每列缺失值数量
    print(
        "\nMissing values per column:\n",
        df.isna().sum().sort_values(ascending=False),
    )

    # 5) 单词是否有重复
    print("\nDuplicate words:", df["word"].duplicated().sum())

    # 6) 随机抽样 15 行
    print("\nSample rows:\n", df.sample(15, random_state=42))


if __name__ == "__main__":
    main()