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
       to_char(d.day, 'YYYY-WW') as week,
       sum(d.visits) as visits,
       sum(d.signups) as signups
from campaign_daily d
join campaign c on c.id = d.campaign_id
group by c.id, c.name, to_char(d.day, 'YYYY-WW');
