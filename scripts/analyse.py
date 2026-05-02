import os 
import numpy as np 
import pandas as pd
from dotenv import load_dotenv
import yfinance as yf

from sqlalchemy import create_engine

load_dotenv()


load_dotenv()

user = os.getenv('DB_user')
password = os.getenv('DB_password')
db_name = os.getenv('DB_name')
engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{db_name}')


def kpi_total_return_2years():
    query = """
    SELECT 
        ticker,
        ROUND(((close_2026 / close_2024) - 1) * 100, 2) as return_pct
    FROM (
        SELECT ticker,
               MAX(CASE WHEN date = '2024-01-02' THEN close END) as close_2024,
               MAX(CASE WHEN date = '2026-01-02' THEN close END) as close_2026
        FROM prices
        WHERE date IN ('2024-01-02', '2026-01-02')
        GROUP BY ticker
    ) t
    WHERE close_2024 IS NOT NULL AND close_2026 IS NOT NULL
    ORDER BY return_pct DESC ; 
    """
    return pd.read_sql(query, engine) 

def kpi_daily_return():
    query = """
    SELECT *, 
       ROUND((((close - prev_close) / prev_close) * 100 ) ::numeric, 4) AS daily_return_pct
FROM (
    SELECT 
        ticker,
        date,
        close,
        LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
    FROM prices
) ; 
    """
    return pd.read_sql(query, engine)



