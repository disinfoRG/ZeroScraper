import scrapy
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_fetch_time
import time
import json


class UpdateDcardPostsSpider(scrapy.Spider):
    name = "dcard_update"
    handle_httpstatus_list = [404]

    def __init__(self, posts_to_update, site_id=None, *args, **kwargs):
        super(UpdateDcardPostsSpider, self).__init__(*args, **kwargs)
        self.selenium = False
        self.posts_to_update = posts_to_update
        self.site_id = site_id
        if site_id:
            self.name = f"{self.name}:{site_id}"

    def start_requests(self):
        for post in self.posts_to_update:
            self.logger.info(f'updating {post["article_id"]}')
            post_id = post["url"].split("/p/")[-1]
            post_api = f"https://www.dcard.tw/_api/posts/{post_id}/"
            last_comment_count = post["last_comment_count"]

            yield scrapy.Request(
                url=post_api,
                callback=self.get_comments,
                cb_kwargs={
                    "post_id": post_id,
                    "last_comment_count": max(
                        0, last_comment_count - 1
                    ),  # so every snapshot has at least 1 comment
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
        now = int(time.time())
        site_type = "discussion_board"

        # populate article item
        # copy from the original article
        article["article_id"] = article_id
        # update
        article["last_snapshot_at"] = now

        if response.status in self.handle_httpstatus_list:
            article["snapshot_count"] = snapshot_count
            article["next_snapshot_at"] = 0
            article_snapshot = None

        else:
            article["snapshot_count"] = snapshot_count + 1
            article["next_snapshot_at"] = generate_next_fetch_time(
                site_type, article["snapshot_count"], now
            )

            # populate article_snapshot item
            post_comments = {"post": post_response, "comments": comment_response}
            article_snapshot["raw_data"] = json.dumps(post_comments)
            article_snapshot["snapshot_at"] = now
            article_snapshot["article_id"] = article_id

        yield {"article": article, "article_snapshot": article_snapshot}
