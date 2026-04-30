import yfinance as yf
import pandas as pd

df = yf.download("AAPL")
print(df) 