from pathlib import Path

from app.database.connection import engine


SCHEMA_PATH = Path(__file__).resolve().parents[3] / "sql" / "schema.sql"


def init_db():
    schema_sql = SCHEMA_PATH.read_text()

    with engine.begin() as conn:
        conn.exec_driver_sql(schema_sql)

    print("Database initialized: prices table is ready.")


if __name__ == "__main__":
    init_db()
