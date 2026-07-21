from os import sync

from app.database.database_service import DatabaseService
from datetime import datetime

db = DatabaseService()
def sync_prices():

    latest_timestamp = db.get_latest_timestamp()

    if latest_timestamp is None:

        start = "2024-01-01"

    else:

        start = latest_timestamp.strftime("%Y-%m-%d")
    print(latest_timestamp)
    end = datetime.now().strftime("%Y-%m-%d")

sync_prices()
