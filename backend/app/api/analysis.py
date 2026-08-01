from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from requests import HTTPError

from app.services.openai_service import OpenAIService

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)

openai_service = OpenAIService()


class AnalysisRequest(BaseModel):
    ticker: str
    date: str
    selected_date: str | None = None
    open_price: float
    close_price: float
    volume: float | None = None
    latest_news: list[dict[str, Any]] = Field(default_factory=list)
    prompt: str


@router.post("")
def create_analysis(request: AnalysisRequest):
    try:
        return openai_service.create_financial_report(request.prompt)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except HTTPError as exc:
        detail = str(exc)
        try:
            detail = exc.response.json().get("error", {}).get("message", detail)
        except ValueError:
            pass

        raise HTTPException(
            status_code=502,
            detail=f"OpenAI request failed: {detail}",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Report generation failed: {exc}",
        )
