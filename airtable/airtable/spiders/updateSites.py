# -*- coding: utf-8 -*-
import scrapy
import json
import os


class UpdatesitesSpider(scrapy.Spider):
    name = "updateSites"
    allowed_domains = ["api.airtable.com"]

    def get_request(self, offset=None):
        url = "https://api.airtable.com/v0/appdh2WkMremF0G1L/Sites?fields=id&fields=name&fields=url&fields=approved&fields=type&filterByFormula=approved&view=List"
        if offset is not None:
            url += f"&offset={offset}"
        return scrapy.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.settings.get('AIRTABLE_API_KEY')}"
            },
            callback=self.parse,
        )

    def start_requests(self):
        yield self.get_request()

    def parse(self, response):
        data = json.loads(response.text)
        for record in data["records"]:
            site = record["fields"]
            if not ("approved" in site and site["approved"]):
                continue
            yield site
        if "offset" in data:
            yield self.get_request(offset=data["offset"])
