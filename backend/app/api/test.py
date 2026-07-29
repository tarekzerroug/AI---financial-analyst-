from dotenv import load_dotenv
import os
import requests
from streamlit.dataframe_util import Data
load_dotenv()


api_key = os.getenv("NEWS_API_KEY")
url = os.getenv("BASE_URL" , "")

params = {
    "function": "NEWS_SENTIMENT",
    "tickers": "AAPL",
    "apikey": api_key,
}

r = requests.get(url, params=params)
data = r.json()
print(data)