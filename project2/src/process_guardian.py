import json
from pathlib import Path


def main():
    # 1. 指向 raw JSON 文件
    raw_path = Path("data/raw/guardian_sample_page1.json")

    if not raw_path.exists():
        raise FileNotFoundError(
            f"找不到 {raw_path}。请先运行 python src/fetch_guardian.py 获取数据。"
        )

    # 2. 读取 JSON
    with raw_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # 3. 取出 results 列表
    try:
        results = data["response"]["results"]
    except KeyError:
        raise KeyError("JSON 中没有找到 ['response']['results'] 字段。")

    print(f"The total number of articles in this page：{len(results)}")

    if not results:
        print("results 为空，没有文章。")
        return

    # 4. 看看第一篇文章的关键字段
    first = results[0]
    print("\n=== Some paragraph on the first passage ===")
    print("id:", first.get("id"))
    print("sectionName:", first.get("sectionName"))
    print("webPublicationDate:", first.get("webPublicationDate"))
    print("webTitle:", first.get("webTitle"))

    fields = first.get("fields", {})
    headline = fields.get("headline", "")
    body_text = fields.get("bodyText", "")

    print("\nheadline:", headline[:100])
    print("\nbodyText the first 200 words：")
    print(body_text[:200])


if __name__ == "__main__":
    main()