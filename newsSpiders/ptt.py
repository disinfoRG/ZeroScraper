import requests
from bs4 import BeautifulSoup
import zlib
import pugsql
import os
import time
import logging
from newsSpiders.helpers import generate_next_snapshot_time

logger = logging.getLogger(__name__)

netloc = "https://www.ptt.cc"


class DiscoverSite:
    def __init__(self, site_info):
        self.queries = pugsql.module("./queries")
        self.queries.connect(os.getenv("DB_URL"))
        self.site_url = site_info["url"]
        self.site_id = site_info["site_id"]

    def db_has(self, url, url_hash):
        if self.queries.get_article_id_by_url(url=url, url_hash=url_hash) is not None:
            return True
        else:
            return False

    def crawl_and_insert(self, article_urls):
        for url in article_urls:
            url_hash = str(zlib.crc32(url.encode()))
            if self.db_has(url, url_hash):
                continue

            now = int(time.time())
            snapshot = requests.get(url, cookies={"over18": "1"}).text
            next_snapshot_at = generate_next_snapshot_time(
                self.site_url, snapshot_count=1, snapshot_time=now
            )

            inserted_article_id = self.queries.insert_article(
                site_id=self.site_id,
                url=url,
                url_hash=url_hash,
                first_snapshot_at=now,
                last_snapshot_at=now,
                next_snapshot_at=next_snapshot_at,
                snapshot_count=1,
                redirect_to=None,
                article_type="PTT",
            )

            self.queries.insert_snapshot(
                article_id=inserted_article_id, snapshot_at=now, raw_data=snapshot
            )
            logger.info(
                f"Finish discover {url}, new article_id = {inserted_article_id}"
            )

    @staticmethod
    def find_new_urls_on_page(page_url, existing_urls):
        r = requests.get(page_url, cookies={"over18": "1"})
        soup = BeautifulSoup(r.text, "html.parser")
        url_elements = [
            x.find("a") for x in soup.find_all("div", {"class": "r-ent"}) if x.find("a")
        ]
        article_urls = [netloc + x["href"] for x in url_elements]
        new_urls = list(set(article_urls) - set(existing_urls))
        prev_page_url = netloc + soup.find_all("a", {"class": "btn wide"})[1]["href"]

        return new_urls, prev_page_url

    def run(self, depth):
        buffer_pages = depth * 0.05
        max_pages = 2 * (depth + int(buffer_pages))
        dedup_limit = 20 * max_pages
        recent_urls_in_db = [
            x["url"]
            for x in self.queries.get_recent_articles_by_site(
                site_id=self.site_id, limit=dedup_limit
            )
        ]
        extra_pages = 0
        d = 0
        page_url = self.site_url
        stop = False

        while not stop:
            new_urls, prev_page_url = self.find_new_urls_on_page(
                page_url, recent_urls_in_db
            )
            self.crawl_and_insert(new_urls)
            d += 1
            page_url = prev_page_url

            if d > depth:
                if not new_urls:
                    extra_pages += 1
                else:
                    extra_pages = 0
            if extra_pages >= buffer_pages:
                stop = True

            logger.info(
                f"Depth: {d}; Consecutive {extra_pages} extra pages with no new urls."
            )

            if d > max_pages:
                stop = True
                logger.info("Reach max pages, stopping.")
