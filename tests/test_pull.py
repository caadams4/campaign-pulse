from pulse.pull import normalise, today_local


def test_normalise_fills_missing_with_zero():
    assert normalise({"date": "2026-04-06", "visits": 9}) == ("2026-04-06", 0, 9, 0, 0)


def test_today_local_is_a_date():
    assert today_local("America/Toronto").year >= 2026
