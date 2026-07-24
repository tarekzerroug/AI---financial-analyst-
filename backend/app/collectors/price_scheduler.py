import os

from apscheduler.schedulers.blocking import BlockingScheduler

from app.collectors.sync_prices import sync_all_prices


def env_bool(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def main():
    timezone = os.getenv("PRICE_SYNC_TIMEZONE", "America/Toronto")
    hour = int(os.getenv("PRICE_SYNC_HOUR", "18"))
    minute = int(os.getenv("PRICE_SYNC_MINUTE", "0"))

    scheduler = BlockingScheduler(timezone=timezone)

    scheduler.add_job(
        sync_all_prices,
        "cron",
        hour=hour,
        minute=minute,
        id="daily_price_sync",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    print(f"Price scheduler started. Daily sync time: {hour:02d}:{minute:02d} {timezone}")

    if env_bool("PRICE_SYNC_RUN_ON_START", True):
        print("Running startup price sync.")
        sync_all_prices()

    scheduler.start()


if __name__ == "__main__":
    main()
