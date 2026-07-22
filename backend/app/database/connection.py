import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SSLMODE = os.getenv("DB_SSLMODE", "require")
DB_CONNECT_TIMEOUT = os.getenv("DB_CONNECT_TIMEOUT", "10")

required_settings = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
}
missing_settings = [
    name for name, value in required_settings.items()
    if not value
]

if missing_settings:
    raise RuntimeError(
        "Missing database environment variables: "
        + ", ".join(missing_settings)
    )

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
    query={
        "sslmode": DB_SSLMODE,
        "connect_timeout": DB_CONNECT_TIMEOUT,
    },
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
