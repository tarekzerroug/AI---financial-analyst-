from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from app.database.connection import engine
from app.database.database_service import DatabaseService

db = DatabaseService()

TICKERS_CSV = Path(__file__).resolve().parents[1] / "data" / "sp500_tickers.csv"


def sync_prices(ticker):
    ticker = ticker.upper()

    latest_timestamp = db.get_latest_timestamp(ticker)

    if latest_timestamp is None:

        start = "2024-01-01"

    else:

        start = (latest_timestamp + timedelta(days=1)).strftime("%Y-%m-%d")

    
    end = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    if start >= end:
        print(f"No new date range for {ticker}: {start} -> {end}")
        return

    data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
    )

    if data.empty:
        print(f"No new data for {ticker}")
        return

    data.reset_index(inplace=True)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data["ticker"] = ticker
    data = data[["Date", "ticker", "Open", "Close", "Volume"]]
    
        
    data.columns = ["date", "ticker", "open", "close", "volume"]
    data.to_sql("prices", engine, if_exists="append", index=False)


def load_tickers():
    tickers = pd.read_csv(TICKERS_CSV)["Symbol"]
    return tickers.dropna().astype(str).str.strip().str.upper().tolist()


def sync_all_prices():
    tickers = load_tickers()
    failures = []

    for ticker in tickers:
        try:
            sync_prices(ticker)
        except Exception as exc:
            failures.append(ticker)
            print(f"Failed to sync {ticker}: {exc}")

    if failures:
        print(f"Price sync completed with {len(failures)} failed ticker(s): {failures}")
    else:
        print("Price sync completed successfully.")


def main():
    sync_all_prices()


if __name__ == "__main__":
    main()
