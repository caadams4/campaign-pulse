import os
import csv
import io

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
import psycopg
from psycopg.rows import dict_row

from pulse import config

app = FastAPI(title="campaign-pulse")


def query(sql, params=()):
    with psycopg.connect(config.load().database_url, row_factory=dict_row) as conn:
        return conn.execute(sql, params).fetchall()


@app.get("/api/daily")
def daily(days: int = 30):
    return query("select * from v_daily_totals where day >= current_date - %s order by day", (days,))


@app.get("/api/channels")
def channels():
    return query("select * from v_channel_rollup")


@app.get("/api/webinars")
def webinars():
    return query("select * from v_webinar_attribution")


@app.get("/api/export.csv")
def export_csv(days: int = 30):
    rows = query("select * from v_daily_totals where day >= current_date - %s order by day", (days,))
    buf = io.StringIO()
    if rows:
        wr = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    return Response(buf.getvalue(), media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=campaign-pulse.csv"})


# keep this last or it swallows the api routes
app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "web"), html=True), name="web")
