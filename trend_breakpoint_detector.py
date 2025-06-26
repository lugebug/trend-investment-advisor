import json
import os
from datetime import datetime
from typing import List, Dict

import pandas as pd

INPUT_FILE = "trend_keywords_output.json"
OUTPUT_FILE = "trend_breakpoint_output.json"


def detect_breakpoint(dates: List[str]) -> bool:
    if not dates:
        return False
    date_series = pd.to_datetime(pd.Series(dates)).dt.normalize()
    counts = date_series.value_counts().sort_index()
    if len(counts) < 4:
        return False
    recent_avg = counts.iloc[-3:].mean()
    past_avg = counts.iloc[:-3].mean() if len(counts) > 3 else 0
    if past_avg == 0:
        return False
    return recent_avg > past_avg * 2


def main() -> None:
    if not os.path.exists(INPUT_FILE):
        print(f"Input file {INPUT_FILE} does not exist. Skipping breakpoint detection.")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        clusters: List[Dict] = json.load(f)
    for cluster in clusters:
        cluster["breakpoint_detected"] = detect_breakpoint(cluster.get("dates", []))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(clusters, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
