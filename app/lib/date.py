from datetime import datetime, timedelta


def date_in_past(days_to_subtract):
    d = datetime.today() - timedelta(days=days_to_subtract)
    return d.strftime("%Y-%m-%d")
