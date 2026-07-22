from os import sync
from app.collectors.fetch_prices import fetch_and_store_price
from app.database.database_service import DatabaseService
from datetime import datetime
import pandas as pd 
from pathlib import Path
import yfinance as yf
from app.database.connection import engine

db = DatabaseService()

TICKERS_CSV = Path(__file__).resolve().parents[1] / "data" / "sp500_tickers.csv"


def sync_prices(ticker):

    latest_timestamp = db.get_latest_timestamp()

    if latest_timestamp is None:

        start = "2024-01-01"

    else:

        start = latest_timestamp.strftime("%Y-%m-%d")
    
    end = datetime.now().strftime("%Y-%m-%d")

    data = yf.download(ticker, start=start, end=end)
    
    data.reset_index(inplace=True)  
    data['ticker'] = ticker
    data = data[["Date", "ticker", "Open", "Close", "Volume"]]
    
        
    data.columns = ["date", "ticker", "open", "close", "volume"]
    data.to_sql("prices", engine, if_exists="append", index=False)


tickers = pd.read_csv(TICKERS_CSV)["Symbol"].tolist()
for ticker in tickers:
    sync_prices(ticker)


print("Data fetching and storing completed.xample ticker, replace with your desired ticker")

