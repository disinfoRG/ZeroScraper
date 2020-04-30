from datetime import datetime, timedelta


def get_article_type(url):
    if "dcard" in url:
        article_type = "Dcard"
    elif "ptt" in url:
        article_type = "PTT"
    else:
        article_type = "Article"
    return article_type


def generate_next_snapshot_time(site_url, snapshot_count, snapshot_time):
    """
    A method that generates next fetch time based on site type
    :param site_url: str, the type of site where articles are from
    :param snapshot_count: int, how many times have this article fetched?
    :param snapshot_time: a unix timestamp
    :return: next_snapshot_time, in unix timestamp
    """
    # turn to datetime object
    parse_time = datetime.fromtimestamp(snapshot_time)

    def time_after(days):
        target_time = parse_time + timedelta(days=days)
        return datetime.timestamp(target_time)

    if "appledaily" in site_url:
        if snapshot_count == 1:
            return time_after(days=0)
        if snapshot_count in range(2, 4):
            return time_after(days=1)
        elif snapshot_count == 4:
            return time_after(days=4)
        else:
            return 0
    else:

        if snapshot_count in range(3):
            return time_after(days=1)
        elif snapshot_count == 3:
            return time_after(days=4)
        else:
            return 0
