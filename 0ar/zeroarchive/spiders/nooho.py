"""
Spider for [怒吼](http://nooho.net)
"""
import scrapy
import re


def match_any(pats, val):
    return any([pat.match(val) for pat in pats])


def parse_item(response):
    return {"url": response.url, "body": response.text}


class Nooho(scrapy.Spider):
    name = "nooho-怒吼文章"
    start_urls = ["https://nooho.net/category/%e6%80%92%e5%90%bc%e6%96%87%e7%ab%a0/"]
    item_patterns = [re.compile("https://nooho.net/\d+/\d+/DPPfraud\d+/")]
    page_patterns = [
        re.compile(
            "https://nooho.net/category/%e6%80%92%e5%90%bc%e6%96%87%e7%ab%a0/page/\d+"
        )
    ]

    def parse(self, response):
        links = [l.attrib["href"] for l in response.css("a")]

        items = [l for l in links if match_any(self.item_patterns, l)]
        pages = [l for l in links if match_any(self.page_patterns, l)]

        for item in items:
            yield response.follow(item, callback=parse_item)

        for page in pages:
            yield response.follow(page, callback=self.parse)
