# 📈 campaign-pulse

Daily Plovercast campaign numbers, in our own Postgres, with a chart page on top.

## 👋 Why this exists

Marketing Ops used to get campaign numbers by someone (usually me) exporting a
CSV from the Plovercast UI every Monday and pasting it into a sheet. Then the
sheet broke, twice, in the same week, and I decided life was too short.

So: a little Python job pulls the numbers from `api.plovercast.com/v3` every
morning, upserts them into Postgres, and a tiny FastAPI app draws a chart. That's
the whole thing. It is deliberately small.

## 🚀 Quick start

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # then fill in the blanks, never commit .env
psql "$PULSE_DATABASE_URL" -f sql/001_schema.sql -f sql/002_views.sql
python -m scripts.load_sample # fake numbers, no API key needed
uvicorn pulse.web:app --port 8000
```

Open http://localhost:8000 and you should see a chart. If you have a real
key in `.env`, `python -m pulse.pull --days 3` pulls the last three days.

## ⚙️ Config

All via environment variables (see `.env.example`, values intentionally empty).

| var | what |
|---|---|
| `PLOVERCAST_API_KEY` | key for the v3 API |
| `PLOVERCAST_BASE_URL` | optional, defaults to the public v3 URL |
| `PULSE_DATABASE_URL` | Postgres connection string |
| `PULSE_TZ` | timezone for "today", default `America/Toronto` |

## 🗂️ What's in the box

| path | what |
|---|---|
| `pulse/plovercast.py` | mini API client (pagination + retry) |
| `pulse/pull.py` | the scheduled job |
| `pulse/web.py` | FastAPI app, serves `web/` and a few JSON endpoints |
| `sql/` | schema + views, run in order |
| `data/sample_campaigns.csv` | invented numbers, any resemblance to real campaigns is a coincidence |
| `web/` | the chart page, hand-rolled canvas, no build step |
| `tests/` | pytest, fake responses only |

## 🧪 Tests

```bash
pytest
```

## 🙏 Thanks

- **Sunniva Oduya** at Plovercast, for patiently explaining cursors and for the
  Retry-After fix. (Yes I know it's morning for you and evening for me, again.)
- **Tomas** for lending me a staging Postgres and not asking why.
- **Kofi** for being my first guinea pig user and telling me the chart was "fine i think".

## 📝 Known stuff

- the chart multiplies signups by 10 so you can see them. yes it's hacky
- no auth on the web app, it only runs inside the VPN
