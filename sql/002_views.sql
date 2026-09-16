-- views the chart page reads from

create or replace view v_daily_totals as
select day,
       sum(impressions) as impressions,
       sum(visits)      as visits,
       sum(clicks)      as clicks,
       sum(signups)     as signups
from campaign_daily
group by day
order by day;

-- weekly per campaign
create or replace view v_campaign_weekly as
select c.id as campaign_id,
       c.name,
       date_trunc('week', d.day)::date as week_start,
       sum(d.visits) as visits,
       sum(d.signups) as signups
from campaign_daily d
join campaign c on c.id = d.campaign_id
group by c.id, c.name, date_trunc('week', d.day);

-- last 30 days by channel
create or replace view v_channel_rollup as
select c.channel,
       sum(d.impressions) as impressions,
       sum(d.visits) as visits,
       sum(d.clicks) as clicks,
       sum(d.signups) as signups,
       round(100.0 * sum(d.signups) / nullif(sum(d.visits), 0), 2) as signup_rate_pct
from campaign_daily d
join campaign c on c.id = d.campaign_id
where d.day >= current_date - 30
group by c.channel
order by visits desc;
