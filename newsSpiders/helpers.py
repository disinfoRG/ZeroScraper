from datetime import datetime, timedelta


def get_article_type(url):
    if "dcard" in url:
        article_type = "Dcard"
    elif "ptt" in url:
        article_type = "PTT"
    else:
        article_type = "Article"
    return article_type


def get_site_type(queries, site_id):
    try:
        r = queries.get_site_by_id(site_id=site_id)
        site_type = r["type"]
    except:
        site_type = None
    return site_type


def generate_next_snapshot_time(site_type, snapshot_count, snapshot_time):
    """
    A method that generates next fetch time based on site type
    :param site_type: str, the type of site where articles are from
    :param snapshot_count: int, how many times have this article fetched?
    :param snapshot_time: a unix timestamp
    :return: next fetch time, in unix timestamp
    """
    # turn to datetime object
    parse_time = datetime.fromtimestamp(snapshot_time)
    # Default
    if 3 > snapshot_count >= 1:
        next_snapshot_time = parse_time + timedelta(days=1)
        return datetime.timestamp(next_snapshot_time)
    elif snapshot_count == 3:
        next_snapshot_time = parse_time + timedelta(days=4)
        return datetime.timestamp(next_snapshot_time)
    else:
        return 0
