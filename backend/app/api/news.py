from fastapi import APIRouter, HTTPException, Query
from dotenv import load_dotenv
from app.services.news_service import news_service
from app.api.utils import filter_json
import os

load_dotenv()

api_key = os.getenv("NEWS_API_KEY")
url = os.getenv("BASE_URL" , "")

news_services = news_service()

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

@router.get("/{ticker}")
def return_news(ticker: str, limit: int = Query(5, ge=1, le=10)):
    fetch_limit = min(max(limit * 3, 10), 50)

    try:
        data = news_services.get_news(
            ticker.upper(),
            api_key,
            url,
            limit=fetch_limit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"News API request failed: {exc}",
        )

    api_error = data.get("Error Message") or data.get("Note") or data.get("Information")
    if api_error:
        raise HTTPException(status_code=502, detail=api_error)

    return filter_json(data, ticker, limit=limit)
