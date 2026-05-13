"""Load data/sample_campaigns.csv so you can click around without an API key."""
import csv
import os
import sys

from pulse import db

PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_campaigns.csv")


def main():
    conn = db.connect(os.environ["PULSE_DATABASE_URL"])
    seen = set()
    with conn.cursor() as cur, open(PATH) as f:
        for r in csv.DictReader(f):
            if r["campaign_id"] not in seen:
                seen.add(r["campaign_id"])
                kind = "webinar" if "Webinar" in r["campaign_name"] else "campaign"
                db.upsert_campaign(cur, {"id": r["campaign_id"], "name": r["campaign_name"],
                                         "channel": r["channel"], "kind": kind})
            db.upsert_daily(cur, r["campaign_id"], (r["day"], int(r["impressions"]), int(r["visits"]),
                                                    int(r["clicks"]), int(r["signups"])))
    conn.commit()
    print("loaded", len(seen), "campaigns", file=sys.stderr)


if __name__ == "__main__":
    main()
