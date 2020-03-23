from dateutil.parser import parse


def get_stats_by_site(queries, site_id):
    result = queries.get_stats_by_site(site_id=site_id)
    result = list(result)
    return result


def get_stats_by_date(queries, date):
    date = parse(date).strftime("%Y-%m-%d")
    result = queries.get_stats_by_date(date=date)
    result = list(result)
    return result


def get_all_stats(queries):
    result = queries.get_all_stats()
    result = list(result)
    return result

