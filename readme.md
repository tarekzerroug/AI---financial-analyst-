# AI Financial Analytics Platform

An AI-powered business intelligence platform for financial market analysis. The app combines historical stock prices from PostgreSQL, relevant financial news, and an LLM reasoning model to generate structured financial reports from a selected ticker and date.

## Features

- React frontend for selecting a ticker and report date
- FastAPI backend with REST endpoints for prices, news, and AI analysis
- PostgreSQL price storage with SQLAlchemy
- APScheduler ETL jobs for incremental market price synchronization
- Alpha Vantage news sentiment integration
- OpenAI Responses API integration for financial report generation
- Docker Compose setup for API and scheduled price sync services
- Frontend can be served directly from FastAPI after build

## Tech Stack

- Frontend: React, Vite, CSS
- Backend: Python, FastAPI
- Database: PostgreSQL, SQLAlchemy, pandas
- ETL: yfinance, APScheduler
- AI: OpenAI Responses API, reasoning model
- Deployment: Docker, AWS EC2, AWS RDS

## Project Structure

```text
.
├── backend/
│   └── app/
│       ├── api/              # FastAPI routes
│       ├── collectors/       # price sync and scheduler jobs
│       ├── database/         # DB connection and query services
│       ├── services/         # news and OpenAI service clients
│       └── main.py           # FastAPI app entrypoint
├── frontend/                 # React/Vite frontend
├── sql/schema.sql            # PostgreSQL schema
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Environment Variables

Create a `.env` file in the project root. Use `.env.exemple` as a starting point.

```env
DB_HOST=
DB_PORT=5432
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_SSLMODE=require
DB_CONNECT_TIMEOUT=10

NEWS_API_KEY=
BASE_URL=https://www.alphavantage.co/query

OPENAI_API_KEY=
REASONING_MODEL=
REASONING_EFFORT=
```

`REASONING_EFFORT` is optional. Leave it empty if your selected model does not support the reasoning effort parameter.

## Database Setup

Create the `prices` table:

```bash
PGPASSWORD="$DB_PASSWORD" psql \
  "host=$DB_HOST port=$DB_PORT dbname=$DB_NAME user=$DB_USER sslmode=${DB_SSLMODE:-require}" \
  -f sql/schema.sql
```

## Local Development

Install backend dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

Build the frontend so FastAPI can serve it:

```bash
cd frontend
npm run build
cd ..
```

Start the FastAPI app:

```bash
cd backend
uvicorn app.main:app --reload --port 8002
```

Open the app:

```text
http://localhost:8002
```

API docs:

```text
http://localhost:8002/docs
```

## Frontend Hot Reload

For frontend-only development:

```bash
cd frontend
npm run dev
```

By default, Vite proxies `/api` to `http://localhost:8002`. To point it somewhere else:

```bash
VITE_API_PROXY_TARGET=http://localhost:8001 npm run dev
```

## API Routes

Primary frontend routes:

| Method | Route | Description |
| --- | --- | --- |
| GET | `/api/prices/{ticker}` | Get historical prices for a ticker |
| GET | `/api/news/{ticker}?limit=5` | Get the most relevant news for a ticker |
| POST | `/api/analysis` | Generate an AI financial report |
| GET | `/health` | API health check |

The frontend sends this shape to `/api/analysis`:

```json
{
  "ticker": "AAPL",
  "date": "2026-07-21",
  "selected_date": "2026-07-21",
  "open_price": 323.13,
  "close_price": 327.74,
  "volume": 41255200,
  "latest_news": [],
  "prompt": "You are an AI financial analyst..."
}
```

The backend returns:

```json
{
  "report": "Structured financial report...",
  "model": "configured-model-name",
  "response_id": "resp_...",
  "usage": {}
}
```

## Price Sync

Run a one-time price sync:

```bash
cd backend
python3 -m app.collectors.sync_prices
```

Run the scheduled sync worker:

```bash
cd backend
python3 -m app.collectors.price_scheduler
```

Scheduler environment variables:

```env
PRICE_SYNC_TIMEZONE=America/Toronto
PRICE_SYNC_HOUR=18
PRICE_SYNC_MINUTE=0
PRICE_SYNC_RUN_ON_START=true
```

## Docker

Build and run the API plus price sync worker:

```bash
docker compose up --build
```

The API is exposed on:

```text
http://localhost:8001
```

## Report Workflow

1. User selects a ticker and date in the React frontend.
2. Frontend fetches price rows from PostgreSQL through `/api/prices/{ticker}`.
3. Frontend selects the matching or closest available trading date.
4. Frontend fetches relevant ticker news from `/api/news/{ticker}?limit=5`.
5. Frontend builds a structured analyst prompt.
6. Frontend posts the prompt and market context to `/api/analysis`.
7. Backend calls the configured OpenAI model and returns a financial report.

## Notes

- News is currently selected by ticker relevance, not by the selected price date.
- If the selected date is not a trading day, the frontend uses the closest available price row.
- This project is for analytics and educational use only. It is not financial advice.

## License

Add your preferred license before publishing publicly.
