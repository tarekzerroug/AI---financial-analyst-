from pathlib import Path

import yfinance as yf
import pandas as pd

from app.database.connection import engine

TICKERS_CSV = Path(__file__).resolve().parents[1] / "data" / "sp500_tickers.csv"

def fetch_and_store_price(ticker):
    data = yf.download(ticker, start="2024-01-01", end="2026-04-29")

    data.reset_index(inplace=True)  
    data['ticker'] = ticker
    data = data[["Date", "ticker", "Open", "Close", "Volume"]]

    # 5. Rename to match PostgreSQL schema
    data.columns = ["date", "ticker", "open", "close", "volume"]
    data.to_sql("prices", engine, if_exists="append", index=False)

    

def main():
    tickers = pd.read_csv(TICKERS_CSV)["Symbol"].tolist()
    for ticker in tickers:
        fetch_and_store_price(ticker)
    print("Data fetching and storing completed.")


if __name__ == "__main__":
    main()
