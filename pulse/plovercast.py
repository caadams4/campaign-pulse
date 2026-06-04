"""Tiny wrapper around the Plovercast v3 API.

Sunniva's plovercast-client does this properly (typed models etc) but we only
need two calls so I kept it small.
"""
import time

import requests

DEFAULT_BASE_URL = "https://api.plovercast.com/v3"


class PlovercastError(Exception):
    pass


class Plovercast:
    def __init__(self, api_key, base_url=DEFAULT_BASE_URL, session=None):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def _get(self, path, params=None):
        url = f"{self.base_url}{path}"
        headers = {"X-Api-Key": self.api_key, "Accept": "application/json"}
        for attempt in range(4):
            resp = self.session.get(url, params=params, headers=headers, timeout=30)
            if resp.status_code == 429 or resp.status_code >= 500:
                time.sleep(2 ** attempt)
                continue
            if resp.status_code >= 400:
                raise PlovercastError(f"{resp.status_code} from {path}: {resp.text[:200]}")
            return resp.json()
        raise PlovercastError(f"gave up on {path}")

    def campaigns(self):
        """All campaigns, following next_cursor until it runs out."""
        cursor = None
        while True:
            page = self._get("/campaigns", {"cursor": cursor} if cursor else None)
            yield from page["items"]
            cursor = page.get("next_cursor")
            if not cursor:
                return

    def daily_metrics(self, campaign_id, start, end):
        data = self._get(
            f"/campaigns/{campaign_id}/metrics",
            {"from": start.isoformat(), "to": end.isoformat(), "granularity": "day"},
        )
        return data["rows"]
