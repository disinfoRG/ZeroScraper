import scrapy
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
import sqlalchemy as db
from newsSpiders.helpers import generate_next_fetch_time, connect_to_db
import time


class UpdateContentsSpider(scrapy.Spider):
    name = "update_contents"

    def __init__(self, site_id=None, selenium=False, *args, **kwargs):
        super(UpdateContentsSpider, self).__init__(*args, **kwargs)

        if not site_id:  # if update all articles in db
            self.selenium = True
        else:  # if specified site_id, follow site config
            self.selenium = selenium

        int_current_time = int(time.time())
        engine, connection, tables = connect_to_db()
        article = tables["Article"]
        self.site = tables["Site"]
        query = db.select(
            [
                article.c.article_id,
                article.c.url,
                article.c.site_id,
                article.c.snapshot_count,
                article.c.article_type,
            ]
        )

        if site_id:
            query = query.where(
                db.and_(
                    article.c.site_id == site_id,
                    article.c.next_snapshot_at != 0,
                    article.c.next_snapshot_at < int_current_time,
                    article.c.article_type.in_(["Article", "PTT"]),
                )
            )

        else:
            query = query.where(
                db.and_(
                    article.c.next_snapshot_at != 0,
                    article.c.next_snapshot_at < int_current_time,
                    article.c.article_type.in_(["Article", "PTT"]),
                )
            )
        self.articles_to_update = [dict(row) for row in connection.execute(query)]
        self.connection = connection

    def start_requests(self):
        for a in self.articles_to_update:
            print(f"updating {a['article_id']}")
            yield scrapy.Request(
                url=a["url"],
                callback=self.update_article,
                cb_kwargs={
                    "article_id": a["article_id"],
                    "site_id": a["site_id"],
                    "snapshot_count": a["snapshot_count"],
                },
            )

    def update_article(self, response, article_id, site_id, snapshot_count):
        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        parse_time = int(time.time())
        query = db.select([self.site.columns.type]).where(
            self.site.columns.site_id == site_id
        )
        site_type = self.connection.execute(query).fetchone()[0]

        # populate article item
        # copy from the original article
        article["article_id"] = article_id
        # update
        article["last_snapshot_at"] = parse_time
        article["snapshot_count"] = snapshot_count + 1
        article["next_snapshot_at"] = generate_next_fetch_time(
            site_type, article["snapshot_count"], parse_time
        )

        # populate article_snapshot item
        article_snapshot["raw_data"] = response.text
        article_snapshot["snapshot_at"] = parse_time
        article_snapshot["article_id"] = article_id

        yield {"article": article, "article_snapshot": article_snapshot}
