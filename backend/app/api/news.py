from fastapi import APIRouter, HTTPException
import requests
from dotenv import load_dotenv
import os
import json
load_dotenv()


router = APIRouter(
    prefix="/news",
    tags=["Prices"]
)
data = {}

api_key = os.getenv("NEWS_API_KEY")
url = os.getenv("BASE_URL" , "")

params = {
    "function": "NEWS_SENTIMENT",
    "tickers": "AAPL",
    "apikey": api_key,
}

@router.get("/{ticker}")
def return_news(ticker):
    params = {
    "function": "NEWS_SENTIMENT",
    "tickers": ticker,
    "apikey": api_key,
    }

    r = requests.get(url, params=params)
    data = r.json()
    return data 
  