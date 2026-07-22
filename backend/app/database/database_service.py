import pandas as pd
from sqlalchemy import text
from datetime import datetime
from app.database.connection import engine

class DatabaseService:

    def get_prices(self, ticker):

        query = text("""
        SELECT *
        FROM prices
        WHERE ticker = :ticker
        ORDER BY date;
        """)
        df = pd.read_sql(query, engine, params={"ticker": ticker.upper()})
        return df
   
    def get_latest_timestamp(self):
        query = text("""
        SELECT MAX(date) AS latest_timestamp
        FROM prices
      
        """)
        result = pd.read_sql(query, engine)
        if result.empty or result['latest_timestamp'].isnull().all():
            return None
        return result['latest_timestamp'].iloc[0]

    def get_all_prices(self):
        query = text("""
        SELECT *
        FROM prices
        ORDER BY ticker, date;
        """)
        return pd.read_sql(query, engine)
