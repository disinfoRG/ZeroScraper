import requests
from bs4 import BeautifulSoup
from article import discover
from types import SimpleNamespace
import pugsql
import os
import argparse
import logging

queries = pugsql.module("./queries")
queries.connect(os.getenv("DB_URL"))

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s %(filename)s %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=os.getenv("LOG_LEVEL", "INFO"),
)
logger = logging.getLogger(__name__)

netloc = "https://www.ptt.cc"


def discover_articles(article_urls):
    for url in article_urls:
        article = SimpleNamespace()
        article.url = url
        article.site_id = args.id
        article.ua = "Mozilla 5.0"
        discover(article)


def find_new_urls_on_page(url, existing_urls):
    r = requests.get(url, cookies={'over18': '1'})
    soup = BeautifulSoup(r.text, 'html.parser')
    url_elements = [x.find('a') for x in soup.find_all('div', {'class': 'r-ent'}) if x.find('a')]
    article_urls = [netloc + x['href'] for x in url_elements]
    new_urls = list(set(article_urls)-set(existing_urls))
    prev_page_url = netloc + soup.find_all('a', {"class": "btn wide"})[1]['href']
    return new_urls, prev_page_url


def main(args):
    buffer_pages = args.depth * 0.05
    dedup_limit = 20 * 1.5 * (args.depth + int(buffer_pages))
    site_url = queries.get_site_by_id(site_id=args.id)["url"]
    recent_urls_in_db = [x['url'] for x in
                         queries.get_recent_articles_by_site(site_id=args.id, limit=dedup_limit)
                         ]
    extra_pages = 0
    d = 0
    page_url = site_url
    stop = False

    while not stop:
        new_urls, prev_page_url = find_new_urls_on_page(page_url, recent_urls_in_db)
        discover_articles(new_urls)
        d += 1
        page_url = prev_page_url

        if d > args.depth:
            if not new_urls:
                extra_pages += 1
            else:
                extra_pages = 0
        if extra_pages >= buffer_pages:
            stop = True
        logger.info(f"Depth: {d}; Consecutive {extra_pages} extra pages with no new urls.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "id", type=int
    )
    parser.add_argument(
        "--depth", type=int, default=200
    )

    args = parser.parse_args()
    main(args)


