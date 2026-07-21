from sqlalchemy import text

from app.database.connection import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))

    print(result.fetchone())