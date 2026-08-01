from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.prices import router as prices_router
from app.api.news import router as news_router

app = FastAPI(
    title="AI Financial Analyst API",
    description="Backend API for AI Financial Analyst",
    version="1.0.0"
)

app.include_router(prices_router)
app.include_router(news_router)
app.include_router(prices_router, prefix="/api")
app.include_router(news_router, prefix="/api")

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIST / "assets"),
        name="frontend-assets",
    )


@app.get("/health")
def health():
    return {
        "message": "AI Financial Analyst API is running "
    }


@app.get("/")
def frontend():
    if FRONTEND_DIST.exists():
        return FileResponse(FRONTEND_DIST / "index.html")

    return {
        "message": "AI Financial Analyst API is running ",
        "frontend": "Run `cd frontend && npm install && npm run build` to serve the UI here."
    }


@app.get("/{path:path}")
def frontend_fallback(path: str):
    if path.startswith(("api/", "prices", "news")):
        raise HTTPException(status_code=404, detail="Not found")

    if FRONTEND_DIST.exists():
        return FileResponse(FRONTEND_DIST / "index.html")

    raise HTTPException(status_code=404, detail="Frontend build not found")
