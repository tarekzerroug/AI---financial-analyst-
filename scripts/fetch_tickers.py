import pandas as pd
import requests
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

tables = pd.read_html(StringIO(response.text)) 

df = tables[0]


df["Symbol"].to_csv("../data/sp500_tickers.csv", index=False)
