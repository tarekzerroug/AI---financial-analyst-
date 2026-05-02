import yfinance as yf
import pandas as pd
ticker = "TSLA"
df =  yf.download(ticker, start="2024-01-01", end="2026-04-29")
print(df) 