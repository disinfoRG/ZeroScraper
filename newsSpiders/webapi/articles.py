from url_normalize import url_normalize


def get_article_by_id(queries, article_id):
    article_entry = queries.get_article_by_id(article_id=article_id)
    snapshot_times = [
        x["snapshot_at"]
        for x in queries.get_article_snapshot_time(article_id=article_id)
    ]
    result = {**article_entry, "snapshot_time": snapshot_times}
    return result


def get_article_by_url(queries, url):
    normalized_url = url_normalize(url)
    url_info = {"input_url": url, "normalized_url": normalized_url}

    article_entry = list(queries.get_article_by_url(url=normalized_url))

    if article_entry:
        result = list()
        for entry in article_entry:
            snapshot_time = [
                x["snapshot_at"]
                for x in queries.get_article_snapshot_time(
                    article_id=entry["article_id"]
                )
            ]
            result.append({**url_info, **entry, "snapshot_time": snapshot_time})
    else:
        result = [{**url_info, "error_message": "url does not exist in the database."}]

    return result
