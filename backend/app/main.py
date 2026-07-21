from fastapi import FastAPI

from app.api.prices import router as prices_router

app = FastAPI(
    title="AI Financial Analyst API",
    description="Backend API for AI Financial Analyst",
    version="1.0.0"
)

app.include_router(prices_router)


@app.get("/")
def root():
    return {
        "message": "AI Financial Analyst API is running 🚀"
    }
