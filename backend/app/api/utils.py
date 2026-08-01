def _number(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _ticker_match(article, ticker):
    ticker = ticker.upper()

    for item in article.get("ticker_sentiment", []):
        if item.get("ticker", "").upper() == ticker:
            return item

    return None


def filter_json(data, ticker, limit=5):
    matches = []
    seen_articles = set()

    for article in data.get("feed", []):
        ticker_data = _ticker_match(article, ticker)
        if not ticker_data:
            continue

        article_keys = {
            (article.get("url") or "").strip().lower(),
            (article.get("title") or "").strip().lower(),
        }
        article_keys.discard("")

        if seen_articles.intersection(article_keys):
            continue

        seen_articles.update(article_keys)

        article["ticker_relevance_score"] = _number(
            ticker_data.get("relevance_score")
        )
        article["ticker_sentiment_score"] = _number(
            ticker_data.get("ticker_sentiment_score")
        )
        article["ticker_sentiment_label"] = ticker_data.get(
            "ticker_sentiment_label"
        )
        matches.append(article)

    matches.sort(
        key=lambda article: (
            article.get("ticker_relevance_score", 0),
            article.get("time_published", ""),
        ),
        reverse=True,
    )

    return matches[:limit]
