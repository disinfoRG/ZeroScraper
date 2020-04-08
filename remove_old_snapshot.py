import pugsql
import os

queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))

article_ids = queries.get_lost_ptt_id()
for aid in article_ids:
    last_snapshot_at = queries.get_article_by_id(article_id=aid)["last_snapshot_at"]
    queries.remove_old_snapshot(article_id=aid, last_snapshot_at=last_snapshot_at)