import time
from flask import request


def get_all_sites(queries):
    return {"body": list(queries.get_sites())}


def get_active_sites(queries):
    return {"body": list(queries.get_active_sites())}


def get_article_count(queries, site_id):
    result = queries.get_site_article_count(site_id=site_id)
    return result


def get_latest_article(queries, site_id):
    result = queries.get_site_latest_article(site_id=site_id)
    return result


def get_articles_discovered_in_interval(queries, site_id):
    now = int(time.time())
    time_start = request.args.get("timeStart", 0)
    time_end = request.args.get("timeEnd", now)
    body = list(
        queries.get_site_articles_discovered_in_interval(
            site_id=site_id, time_start=time_start, time_end=time_end
        )
    )
    return {"body": body}


def get_articles_updated_in_interval(queries, site_id):
    now = int(time.time())
    time_start = request.args.get("timeStart", 0)
    time_end = request.args.get("timeEnd", now)
    body = list(
        queries.get_site_articles_updated_in_interval(
            site_id=site_id, time_start=time_start, time_end=time_end
        )
    )
    return {"body": body}
