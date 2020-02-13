def get_article_count(queries, site_id):
    result = queries.get_site_article_count(site_id=site_id)
    return result


def get_latest_article(queries, site_id):
    result = queries.get_site_latest_article(site_id=site_id)
    return result
