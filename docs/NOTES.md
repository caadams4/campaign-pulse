# notes

scratch space, not polished

## plovercast api
- v3 base: `https://api.plovercast.com/v3`
- auth is the `X-Api-Key` header
- `/campaigns` is cursor paginated, `/campaigns/{id}/metrics` takes from/to/granularity
- rate limit is roughly 60 req/min, 429s come with Retry-After
- v2 is being switched off sometime in august, date TBD, we are already on v3 so nothing to do

## numbers that don't match
- Plovercast UI shows visits in the viewer's timezone, API is UTC. see MKT-214
- webinar registrations can lag a day
