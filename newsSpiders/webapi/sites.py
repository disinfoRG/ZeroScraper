def get_article_count(queries, site_id):
    result = queries.get_site_article_count(site_id=site_id)
    return result


def get_latest_article(queries, site_id):
    result = queries.get_site_latest_article(site_id=site_id)
    return result


def get_article_count_in_interval(queries, site_id, discover_from, discover_until):
    result = queries.count_site_article_discovered_in_interval(
        site_id=site_id, discover_from=discover_from, discover_until=discover_until
    )
    return result
