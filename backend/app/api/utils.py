def filter_json(data, ticker):
    return [
        article
        for article in data.get("feed", [])
        if article.get("ticker") == ticker
    ]