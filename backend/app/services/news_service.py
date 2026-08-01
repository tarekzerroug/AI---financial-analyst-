import requests


class news_service:
    

    def get_news(self, ticker, api_key, url, limit=5):
        if not api_key:
            raise ValueError("Missing NEWS_API_KEY")

        if not url:
            raise ValueError("Missing BASE_URL")

        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "sort": "RELEVANCE",
            "limit": limit,
            "apikey": api_key,
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
