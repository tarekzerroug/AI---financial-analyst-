to launch the app on localhost 

cd "/Users/zerroug/Desktop/AI - financial analys/AI---financial-analyst-/backend"
../.venv/bin/python -m uvicorn app.main:app --reload --port 8001

to launch the script to fetch the prices 

cd "/Users/zerroug/Desktop/AI - financial analys/AI---financial-analyst-/backend/app/data"
../../../.venv/bin/python ../../../scripts/fetch_prices.py

to sync the prices: 

cd "/Users/zerroug/Desktop/AI - financial analys/AI---financial-analyst-/backend"
../.venv/bin/python -m app.collectors.sync_prices

cd "/Users/zerroug/Desktop/AI - financial analys/AI---financial-analyst-/backend"
../.venv/bin/python -m app.database.test_connection

python3 -m app.collectors.sync_prices

set -a; source ../.env; set +a; PGPASSWORD="$DB_PASSWORD" /opt/homebrew/opt/postgresql@18/bin/psql -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -U "$DB_USER" "sslmode=${DB_SSLMODE:-require}"