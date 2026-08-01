import requests
import json


class news_service:
    

    def get_news(self, ticker , api_key , url ):

        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "apikey": api_key,
            }
        
        r = requests.get(url, params=params)
        data = r.json()
    
        print(json.dumps(data, indent=4))
        return data 