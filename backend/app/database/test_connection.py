from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from app.database.connection import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print(result.fetchone())
except OperationalError as error:
    print("Database connection failed.")
    print("This usually means the RDS instance is not reachable from your machine.")
    print("Check whether the database is private, requires a VPN/bastion, or blocks your IP in the security group.")
    print(error)