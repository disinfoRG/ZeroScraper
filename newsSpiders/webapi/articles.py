import pugsql
from url_normalize import url_normalize
import os
from dotenv import load_dotenv

load_dotenv()
queries = pugsql.module("queries")


def get_article_by_id(article_id):
    queries.connect(os.getenv("DB_URL"))

    article_entry = queries.get_article_by_id(article_id=article_id)
    snapshot_times = [
        x["snapshot_at"]
        for x in queries.get_article_snapshot_time(article_id=article_id)
    ]
    result = {**article_entry, "snapshot_time": snapshot_times}

    queries.disconnect()
    return result


def get_article_by_url(url):
    queries.connect(os.getenv("DB_URL"))

    normalized_url = url_normalize(url)
    url_info = {"input_url": url, "normalized_url": normalized_url}
    try:
        article_entry = queries.get_article_by_url(url=normalized_url)
        snapshot_time = [
            x["snapshot_at"]
            for x in queries.get_article_snapshot_time(
                article_id=article_entry["article_id"]
            )
        ]
        result = {**url_info, **article_entry, "snapshot_time": snapshot_time}
    except TypeError:
        result = {**url_info, "error message": "url does not exist in the database."}
    queries.disconnect()

    return result
