to build the frontend:

cd frontend
npm install
npm run build

then launch the fast api server:

cd ../backend
uvicorn app.main:app --reload --port 8002

open:

http://localhost:8002

for frontend development with hot reload:

cd frontend
npm run dev

if the api is not on port 8002:

VITE_API_PROXY_TARGET=http://localhost:8001 npm run dev

the frontend reads:

GET /prices/{ticker}
GET /news/{ticker}
POST /analysis

if /analysis is not ready yet, the app still shows the LLM prompt payload.


set -a
source ../.env
set +a

PGPASSWORD="$DB_PASSWORD" /opt/homebrew/opt/postgresql@18/bin/psql \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -d "$DB_NAME" \
  -U "$DB_USER" \
  "sslmode=${DB_SSLMODE:-require}"
