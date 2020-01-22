import scrapy
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_fetch_time
import time
import os
import json
import pugsql

queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))


class UpdateDcardPostsSpider(scrapy.Spider):
    name = "dcard_update"

    def __init__(self, *args, **kwargs):
        super(UpdateDcardPostsSpider, self).__init__(*args, **kwargs)
        self.selenium = False
        int_current_time = int(time.time())
        self.posts_to_update = [
            dict(row)
            for row in queries.get_dcard_posts_to_update(current_time=int_current_time)
        ]

    def start_requests(self):
        for post in self.posts_to_update:
            post_id = post["url"].split("/p/")[-1]
            post_api = f"https://www.dcard.tw/_api/posts/{post_id}/"
            # retrieve last comment count
            last_snapshot_raw_data = queries.get_post_latest_snapshot(
                article_id=post["article_id"]
            )["raw_data"]
            last_snapshot_comments = json.loads(last_snapshot_raw_data)["comments"]
            last_comment_count = last_snapshot_comments[-1]["floor"]

            yield scrapy.Request(
                url=post_api,
                callback=self.get_comments,
                cb_kwargs={
                    "post_id": post_id,
                    "last_comment_count": last_comment_count,
                    "article_id": post["article_id"],
                    "snapshot_count": post["snapshot_count"],
                },
            )

    def get_comments(
        self, response, post_id, last_comment_count, article_id, snapshot_count
    ):
        post_response = json.loads(response.body.decode("utf-8"))
        comment_api = f"https://www.dcard.tw/_api/posts/{post_id}/comments?after={last_comment_count}"

        yield scrapy.Request(
            url=comment_api,
            callback=self.update_post,
            cb_kwargs={
                "post_response": post_response,
                "article_id": article_id,
                "snapshot_count": snapshot_count,
            },
        )

    def update_post(self, response, post_response, article_id, snapshot_count):
        comment_response = json.loads(response.body.decode("utf-8"))

        # init
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        crawl_time = int(time.time())
        site_type = "discussion_board"

        # populate article item
        # copy from the original article
        article["article_id"] = article_id
        # update
        article["last_snapshot_at"] = crawl_time
        article["snapshot_count"] = snapshot_count + 1
        article["next_snapshot_at"] = generate_next_fetch_time(
            site_type, article["snapshot_count"], crawl_time
        )

        # populate article_snapshot item
        post_comments = {"post": post_response, "comments": comment_response}
        article_snapshot["raw_data"] = json.dumps(post_comments)
        article_snapshot["snapshot_at"] = crawl_time
        article_snapshot["article_id"] = article_id

        yield {"article": article, "article_snapshot": article_snapshot}
