import psycopg


def connect(url):
    return psycopg.connect(url)


def upsert_campaign(cur, c):
    cur.execute(
        """
        insert into campaign (id, name, channel, kind, started_on)
        values (%s, %s, %s, %s, %s)
        on conflict (id) do update
          set name = excluded.name, channel = excluded.channel, kind = excluded.kind
        """,
        (c["id"], c["name"], c.get("channel"), c.get("kind", "campaign"), c.get("started_on")),
    )


def archive_missing(cur, live_ids):
    cur.execute("update campaign set status = 'archived' where not (id = any(%s))", (list(live_ids),))


def upsert_daily(cur, campaign_id, row):
    cur.execute(
        """
        insert into campaign_daily (campaign_id, day, impressions, visits, clicks, signups)
        values (%s, %s, %s, %s, %s, %s)
        on conflict (campaign_id, day) do update
          set impressions = excluded.impressions, visits = excluded.visits,
              clicks = excluded.clicks, signups = excluded.signups
        """,
        (campaign_id, *row),
    )
