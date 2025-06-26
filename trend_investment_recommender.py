import json
<<<<<<< 5sevi8-codex/开发趋势分析与投资推荐系统
import os
=======
>>>>>>> main
from typing import Dict, List

INPUT_FILE = "trend_breakpoint_output.json"
OUTPUT_FILE = "trend_recommendations.json"

KEYWORD_TO_TICKERS: Dict[str, List[str]] = {
    "ai": ["NVDA", "QQQ"],
    "芯片": ["NVDA", "AMD"],
    "能源": ["XLE", "CVX"],
    "电动车": ["TSLA"],
    "solar": ["TAN"],
}


def recommend_for_keywords(keywords: List[str]) -> List[str]:
    rec: List[str] = []
    for word in keywords:
        key = word.lower()
        if key in KEYWORD_TO_TICKERS:
            rec.extend(KEYWORD_TO_TICKERS[key])
    return sorted(set(rec))


def main() -> None:
<<<<<<< 5sevi8-codex/开发趋势分析与投资推荐系统
    if not os.path.exists(INPUT_FILE):
        print(f"Input file {INPUT_FILE} does not exist. Skipping recommendations.")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return
=======
>>>>>>> main
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        clusters = json.load(f)
    for cluster in clusters:
        rec = recommend_for_keywords(cluster.get("keywords", []))
        cluster["recommendation"] = rec
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(clusters, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
