-- webinar attribution
-- idea: a webinar gets credit for its own signups, plus "assist" visits from
-- email/linkedin/content campaigns in the 14 days before it was held.
-- (Plovercast's own attribution report uses 30 days, but 14 is what lines up
-- with their UI for us. don't ask.)

create table if not exists webinar_event (
    campaign_id  text primary key references campaign (id),
    held_on      date not null
);

create or replace view v_webinar_attribution as
select w.campaign_id,
       c.name,
       w.held_on,
       coalesce(own.signups, 0)  as registrations,
       coalesce(own.visits, 0)   as own_visits,
       coalesce(assist.visits, 0) as assist_visits,
       coalesce(assist.channels, 0) as assist_channels
from webinar_event w
join campaign c on c.id = w.campaign_id
left join lateral (
    select sum(signups) as signups, sum(visits) as visits
    from campaign_daily d
    where d.campaign_id = w.campaign_id
) own on true
left join lateral (
    select sum(d.visits) as visits, count(distinct c2.channel) as channels
    from campaign_daily d
    join campaign c2 on c2.id = d.campaign_id
    where c2.kind = 'campaign'
      and d.day between w.held_on - 14 and w.held_on
) assist on true
order by w.held_on;
