"""Pull yesterday-ish numbers from Plovercast into postgres."""
import os
import argparse
import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from pulse.plovercast import Plovercast
from pulse import db


def normalise(row):
    return (
        row["date"],
        row.get("impressions", 0),
        row.get("visits", 0),
        row.get("clicks", 0),
        row.get("signups", 0),
    )


def today_local(tz):
    return datetime.now(ZoneInfo(tz)).date()


def run(client, conn, days, tz="America/Toronto", since=None):
    end = today_local(tz)
    start = since or end - timedelta(days=days)
    with conn.cursor() as cur:
        for c in client.campaigns():
            db.upsert_campaign(cur, c)
            for row in client.daily_metrics(c["id"], start, end) or []:
                db.upsert_daily(cur, c["id"], normalise(row))
    conn.commit()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3)
    ap.add_argument("--since", type=date.fromisoformat, help="backfill from this date (YYYY-MM-DD)")
    args = ap.parse_args()
    logging.basicConfig(level=os.environ.get("PULSE_LOG_LEVEL") or "INFO")
    client = Plovercast(os.environ["PLOVERCAST_API_KEY"])
    conn = db.connect(os.environ["PULSE_DATABASE_URL"])
    run(client, conn, args.days, os.environ.get("PULSE_TZ") or "America/Toronto", args.since)
    logging.info("pull finished")  # TODO: store the raw json somewhere so we can replay it


if __name__ == "__main__":
    main()
