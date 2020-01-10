import os
import pugsql
from scrapy.exceptions import DropItem
import sqlalchemy as db
from sqlalchemy.sql.expression import bindparam
from newsSpiders.helpers import connect_to_db


class DuplicatesPipeline:
    def __init__(self):
        self.queries = pugsql.module("queries")

    def open_spider(self, spider):
        self.queries.connect(os.getenv("DB_URL"))

    def process_item(self, item, spider):
        if spider.name == "discover_new_articles":
            if (
                self.queries.get_article_by_url(
                    url=item["article"]["url"], url_hash=item["article"]["url_hash"]
                )
                is not None
            ):
                # XXX for shorter log messages
                item["article_snapshot"]["raw_data"] = "<removed>"
                raise DropItem(f"Duplicate item: {item['article']['url']}")
            else:
                return item
        else:
            return item


class MySqlPipeline(object):
    def __init__(self):
        self.connection = None
        self.db_tables = None
        self.values_list = None
        self.update_article_query = None

    def open_spider(self, spider):
        engine, connection, tables = connect_to_db()
        self.connection = connection
        self.db_tables = {
            "article": tables["Article"],
            "article_snapshot": tables["ArticleSnapshot"],
        }
        self.update_article_query = (
            self.db_tables["article"]
            .update()
            .where(self.db_tables["article"].c.article_id == bindparam("id"))
        )
        self.update_article_query = self.update_article_query.values(
            {
                "snapshot_count": bindparam("snapshot_count"),
                "last_snapshot_at": bindparam("last_snapshot_at"),
                "next_snapshot_at": bindparam("next_snapshot_at"),
            }
        )

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if spider.name == "discover_new_articles":
            query = db.insert(self.db_tables["article"])
            exe = self.connection.execute(query, item["article"])
            article_id = exe.inserted_primary_key
            item["article_snapshot"]["article_id"] = article_id
            query = db.insert(self.db_tables["article_snapshot"])
            self.connection.execute(query, item["article_snapshot"])

        elif spider.name == "update_contents":
            # update Article
            article_dict = dict(item["article"])
            article_dict["id"] = article_dict.pop(
                "article_id"
            )  # because cannot use article_id in bindparam
            self.connection.execute(self.update_article_query, article_dict)

            # insert to ArticleSnapshot
            query = db.insert(self.db_tables["article_snapshot"])
            self.connection.execute(query, item["article_snapshot"])
