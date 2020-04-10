import requests
from bs4 import BeautifulSoup
from article import discover
from types import SimpleNamespace
import pugsql
import os
import argparse

queries = pugsql.module("./queries")
queries.connect(os.getenv("DB_URL"))

netloc = "https:/www.ptt.cc"


def get_website(url):
    r = requests.get(url, cookies={'over18': '1'})
    return r


def collect_article_urls(args):
    article_urls = list()
    target_url = args.url
    for d in range(args.depth):
        r = get_website(target_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        article_urls += [netloc + x.find('a')['href'] for x in soup.find_all('div', {'class': 'r-ent'})]
        print(target_url)
        target_url = netloc + soup.find_all('a', {"class": "btn wide"})[1]['href']
    return article_urls


def main(args):
    site_url = queries.get_site_by_id(site_id=args.site_id)["url"]
    args.url = site_url
    article_urls = collect_article_urls(args)
    recent_urls_in_db = [x['url'] for x in
                         queries.get_recent_articles_by_site(site_id=args.site_id, limit=args.dedup_limit)
                         ]

    article_urls = list(set(article_urls)-set(recent_urls_in_db))

    for url in article_urls:
        article = SimpleNamespace()
        article.url = url
        article.site_id = args.site_id
        discover(article)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "site_id", type=int
    )
    parser.add_argument(
        "--depth", type=int, default=200
    )
    parser.add_argument(
        "--dedup_limit", type=int, default=2000
    )
    args = parser.parse_args()
    main(args)


