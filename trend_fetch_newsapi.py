import os
import json
from datetime import datetime, timedelta
from typing import List, Dict

import requests
from googletrans import Translator

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
KEYWORDS = ["AI", "芯片", "能源"]
OUTPUT_FILE = "trend_news_window.json"


def fetch_news_for_keyword(keyword: str) -> List[Dict]:
    """Fetch news articles for a single keyword."""
    if not NEWSAPI_KEY:
        raise ValueError("NEWSAPI_KEY environment variable not set")

    from_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keyword,
        "from": from_date,
        "sortBy": "publishedAt",
        "pageSize": 100,
        "apiKey": NEWSAPI_KEY,
        "language": "en",
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("articles", [])


def translate_titles(articles: List[Dict], translator: Translator, keyword: str) -> List[Dict]:
    """Translate article titles to Chinese."""
    processed = []
    for art in articles:
        title = art.get("title", "")
        translated_title = translator.translate(title, dest="zh-cn").text if title else ""
        processed.append({
            "keyword": keyword,
            "title": title,
            "translated_title": translated_title,
            "publishedAt": art.get("publishedAt", ""),
        })
    return processed


def main() -> None:
    translator = Translator()
    all_articles: List[Dict] = []
    for kw in KEYWORDS:
        try:
            raw_articles = fetch_news_for_keyword(kw)
            translated = translate_titles(raw_articles, translator, kw)
            all_articles.extend(translated)
        except Exception as exc:
            print(f"Failed to fetch for {kw}: {exc}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
