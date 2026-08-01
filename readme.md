to launch the fast api server : uvicorn app.main:app --reload --port 8002


set -a
source ../.env
set +a

PGPASSWORD="$DB_PASSWORD" /opt/homebrew/opt/postgresql@18/bin/psql \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -d "$DB_NAME" \
  -U "$DB_USER" \
  "sslmode=${DB_SSLMODE:-require}"