from lib.date import date_in_past
from datetime import datetime


def test_date_in_past():
    now = datetime.today().strftime("%Y-%m-%d")

    d = date_in_past(0)
    assert d == now
