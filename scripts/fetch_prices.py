import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('DB_user')
password = os.getenv('DB_password')
db_name = os.getenv('DB_name')
engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{db_name}')

def fetch_and_store_price(ticker):
    data = yf.download(ticker, start="2024-01-01", end="2026-04-29")

    data.reset_index(inplace=True)  
    data['ticker'] = ticker
    data = data[["Date", "ticker", "Open", "Close", "Volume"]]

    # 5. Rename to match PostgreSQL schema
    data.columns = ["date", "ticker", "open", "close", "volume"]
    data.to_sql("prices", engine, if_exists="append", index=False)

    

def main():
    tickers = pd.read_csv("../data/sp500_tickers.csv")["Symbol"].tolist()
    for ticker in tickers:
        fetch_and_store_price(ticker)
    print("Data fetching and storing completed.")
main()
