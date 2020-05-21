import scrapy
from newsSpiders.items import ArticleItem, ArticleSnapshotItem
from newsSpiders.helpers import generate_next_snapshot_time
import time


class BasicUpdateSpider(scrapy.Spider):
    name = "basic_update"
    handle_httpstatus_list = [404, 500]

    def __init__(
        self,
        articles_to_update,
        site_id=None,
        site_url=None,
        selenium=False,
        *args,
        **kwargs,
    ):
        super(BasicUpdateSpider, self).__init__(*args, **kwargs)
        self.articles_to_update = articles_to_update
        self.site_id = site_id
        self.site_url = site_url
        # always start selenium if updating all sites
        self.selenium = selenium if site_id else True
        # for logging
        self.name = f"{self.name}:{site_id}"

    def start_requests(self):
        for a in self.articles_to_update:
            self.logger.info(f"updating {a['article_id']}")
            yield scrapy.Request(
                url=a["url"],
                callback=self.update_article,
                cb_kwargs={
                    "article_id": a["article_id"],
                    "snapshot_count": a["snapshot_count"],
                },
            )

    def update_article(self, response, article_id, snapshot_count):
        article = ArticleItem()
        article_snapshot = ArticleSnapshotItem()
        now = int(time.time())

        article["article_id"] = article_id
        article["last_snapshot_at"] = now

        if response.status in self.handle_httpstatus_list:
            article["snapshot_count"] = snapshot_count
            article["next_snapshot_at"] = 0
            article_snapshot = None
        else:
            article["snapshot_count"] = snapshot_count + 1
            article["next_snapshot_at"] = generate_next_snapshot_time(
                self.site_url, article["snapshot_count"], now
            )

            article_snapshot["raw_data"] = response.text
            article_snapshot["snapshot_at"] = now
            article_snapshot["article_id"] = article_id

        yield {"article": article, "article_snapshot": article_snapshot}
