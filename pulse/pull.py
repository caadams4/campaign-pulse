"""Pull yesterday-ish numbers from Plovercast into postgres."""
import os
import argparse
from datetime import date, timedelta

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


def run(client, conn, days):
    end = date.today()
    start = end - timedelta(days=days)
    with conn.cursor() as cur:
        for c in client.campaigns():
            db.upsert_campaign(cur, c)
            for row in client.daily_metrics(c["id"], start, end):
                db.upsert_daily(cur, c["id"], normalise(row))
    conn.commit()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3)
    args = ap.parse_args()
    client = Plovercast(os.environ["PLOVERCAST_API_KEY"])
    conn = db.connect(os.environ["PULSE_DATABASE_URL"])
    run(client, conn, args.days)
    print("done")  # TODO: store the raw json somewhere so we can replay it


if __name__ == "__main__":
    main()
