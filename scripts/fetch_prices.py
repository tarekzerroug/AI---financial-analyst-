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

