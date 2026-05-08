-- campaign-pulse schema. run with psql -f, it is safe to re-run

create table if not exists campaign (
    id          text primary key,
    name        text not null,
    channel     text,
    kind        text not null default 'campaign',   -- 'campaign' or 'webinar'
    started_on  date
);

create table if not exists campaign_daily (
    campaign_id  text not null references campaign (id),
    day          date not null,
    impressions  integer not null default 0,
    visits       integer not null default 0,
    clicks       integer not null default 0,
    signups      integer not null default 0,
    primary key (campaign_id, day)
);

create index if not exists campaign_daily_day_idx on campaign_daily (day);
