import json

import os

try:
    import pandas as pd
except ImportError:  # pragma: no cover - dependency missing
    pd = None  # type: ignore

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
except ImportError:  # pragma: no cover - dependency missing
    TfidfVectorizer = None  # type: ignore
    KMeans = None  # type: ignore


INPUT_FILE = "trend_news_window.json"
OUTPUT_FILE = "trend_keywords_output.json"
NUM_CLUSTERS = 5


def main() -> None:
    if pd is None or TfidfVectorizer is None or KMeans is None:
        print("Required packages are missing. Skipping analysis.")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return
    if not os.path.exists(INPUT_FILE):
        print(f"Input file {INPUT_FILE} does not exist. Skipping analysis.")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)
    if not articles:
        print("No articles to analyze")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


    titles = [a.get("translated_title", "") for a in articles]
    vectorizer = TfidfVectorizer(max_df=0.8, stop_words="english")
    matrix = vectorizer.fit_transform(titles)

    # use explicit n_init for broader scikit-learn compatibility
    kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42, n_init=10)

    labels = kmeans.fit_predict(matrix)

    features = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

    df = pd.DataFrame(articles)
    df["cluster"] = labels

    result = []
    for cluster_id in sorted(df["cluster"].unique()):
        group = df[df["cluster"] == cluster_id]
        keywords = [features[ind] for ind in order_centroids[cluster_id][:10]]
        trend_score = float(len(group))
        result.append({
            "cluster": int(cluster_id),
            "keywords": keywords,
            "trend_score": trend_score,
            "dates": group["publishedAt"].tolist(),
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
