import pugsql
import os
from dotenv import load_dotenv

load_dotenv()
queries = pugsql.module("queries")


def get_article_count(site_id):
    queries.connect(os.getenv("DB_URL"))
    result = queries.get_site_article_count(site_id=site_id)
    queries.disconnect()
    return result


def get_latest_article(site_id):
    queries.connect(os.getenv("DB_URL"))
    result = queries.get_site_latest_article(site_id=site_id)
    queries.disconnect()
    return result
