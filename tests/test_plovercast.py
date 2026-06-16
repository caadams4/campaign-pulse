import json
import os
from datetime import date

import pytest

from pulse.plovercast import Plovercast, PlovercastError

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def fixture(name):
    with open(os.path.join(FIX, name)) as f:
        return json.load(f)


class FakeResp:
    def __init__(self, status, body, headers=None):
        self.status_code = status
        self._body = body
        self.text = json.dumps(body)
        self.headers = headers or {}

    def json(self):
        return self._body


class FakeSession:
    """Hands back canned responses in order and remembers what was asked."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls.append((url, params))
        return self.responses.pop(0)


def test_campaigns_follows_cursor():
    s = FakeSession([FakeResp(200, fixture("campaigns_page1.json")), FakeResp(200, fixture("campaigns_page2.json"))])
    got = list(Plovercast("example-key", session=s).campaigns())
    assert [c["id"] for c in got] == ["cmp_1001", "cmp_1002", "cmp_1003"]
    assert s.calls[1][1] == {"cursor": "c_page2"}


def test_daily_metrics_rows():
    s = FakeSession([FakeResp(200, fixture("metrics.json"))])
    rows = Plovercast("example-key", session=s).daily_metrics("cmp_1001", date(2026, 4, 6), date(2026, 4, 7))
    assert len(rows) == 2 and rows[0]["visits"] == 96


def test_4xx_raises():
    s = FakeSession([FakeResp(403, {"error": "nope"})])
    with pytest.raises(PlovercastError):
        list(Plovercast("example-key", session=s).campaigns())
