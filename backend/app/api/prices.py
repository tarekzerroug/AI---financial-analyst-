from fastapi import APIRouter, HTTPException

from app.database.database_service import DatabaseService

router = APIRouter(
    prefix="/prices",
    tags=["Prices"]
)

db = DatabaseService()


@router.get("/{ticker}")
def get_prices(ticker: str):

    ticker = ticker.upper()

    prices = db.get_prices(ticker)

    if prices.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No prices found for ticker '{ticker}'"
        )

    return prices.to_dict(orient="records")

@router.get("")
def get_all_prices():
    prices = db.get_all_prices()

    if prices.empty:
        raise HTTPException(
            status_code=404,
            detail="No prices found"
        )

    return prices.to_dict(orient="records")
