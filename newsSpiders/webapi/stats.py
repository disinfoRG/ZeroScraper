from dateutil.parser import parse
from flask import request


def get_stats(queries):
    site_id = request.args.get("site_id", None)
    date = request.args.get("date", None)
    if site_id:
        site_id = int(site_id)
        body = list(queries.get_stats_by_site(site_id=site_id))
    elif date:
        date = parse(date).strftime("%Y-%m-%d")
        body = list(queries.get_stats_by_date(date=date))
    else:
        body = list(queries.get_all_stats())

    return {'body': body}
