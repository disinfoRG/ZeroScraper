# -*- coding: utf-8 -*-
import scrapy
import json
import os
from scrapy.loader import ItemLoader
from airtable.items import SiteItem, site_config_fields


class UpdatesitesSpider(scrapy.Spider):
    name = "updateSites"
    allowed_domains = ["api.airtable.com"]

    def get_request(self, offset=None):
        req_fields = [
            "id",
            "approved",
            "name",
            "url",
            "type",
            "article",
            "following",
            "depth",
            "delay",
            "ua",
            "selenium",
        ]
        url = (
            "https://api.airtable.com/v0/appdh2WkMremF0G1L/Sites?"
            + "&".join([f"fields={f}" for f in req_fields])
            + "&filterByFormula=approved&view=List"
            + (f"&offset={offset}" if offset is not None else "")
        )
        return scrapy.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.settings.get('AIRTABLE_API_KEY')}"
            },
            callback=self.parse,
        )

    def start_requests(self):
        yield self.get_request()

    def parse_record(self, record):
        loader = ItemLoader(item=SiteItem())
        fields = record["fields"]
        return SiteItem(
            {
                "airtable_id": fields["id"],
                "approved": fields["approved"],
                "name": fields["name"],
                "url": fields["url"],
                "type": fields["type"],
                "config": {k: fields[k] for k in site_config_fields if k in fields},
                "site_info": {},
            }
        )

    def parse(self, response):
        data = json.loads(response.text)
        for record in data["records"]:
            site = self.parse_record(record)
            if not ("approved" in site and site["approved"]):
                continue
            yield site
        if "offset" in data:
            yield self.get_request(offset=data["offset"])
