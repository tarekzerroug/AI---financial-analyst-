from fastapi import APIRouter, HTTPException
import requests
from dotenv import load_dotenv
from app.services.news_service import news_service
from app.api.utils import filter_json
import os
import json
load_dotenv()

api_key = os.getenv("NEWS_API_KEY")
url = os.getenv("BASE_URL" , "")

news_services = news_service()

router = APIRouter(
    prefix="/news",
    tags=["Prices"]
)
data = {}



params = {
    "function": "NEWS_SENTIMENT",
    "tickers": "AAPL",
    "apikey": api_key,
}

@router.get("/{ticker}")
def return_news(ticker):
    data = news_services.get_news(ticker , api_key , url)
    filtered_data = filter_json(data, ticker)
    return filtered_data
