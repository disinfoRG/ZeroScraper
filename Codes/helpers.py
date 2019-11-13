from datetime import datetime, timedelta


def generate_next_fetch_time(site_type, fetch_count, parse_time):
    """
    A method that generates next fetch time based on site type
    :param site_type: str, the type of site where articles are from
    :param fetch_count: int, how many times have this article fetched?
    :param parse_time: a datetime object of the current parse time
    :return: next fetch time, in string format
    """

    if site_type == 'content_farm':
        # 1/day for 1 week, 1/week for 1 month
        if 11 > fetch_count >= 7:
            return (parse_time + timedelta(weeks=1)).strftime('%Y-%m-%d-%H:%M:%S')
        elif 7 > fetch_count >= 1:
            return (parse_time + timedelta(days=1)).strftime('%Y-%m-%d-%H:%M:%S')
        else:
            return None  # todo: or max time?

    elif site_type == 'news_websites':
        # 1/hour for 1 day
        if fetch_count < 24:
            return (parse_time + timedelta(hours=1)).strftime('%Y-%m-%d-%H:%M:%S')
        else:
            return None
    elif site_type == 'organization_website':
        # todo: what's the update frequency of organization website?
        if 7 > fetch_count >= 1:
            return (parse_time + timedelta(days=1)).strftime('%Y-%m-%d-%H:%M:%S')
