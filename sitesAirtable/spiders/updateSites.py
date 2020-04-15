# -*- coding: utf-8 -*-
import scrapy
import json
from sitesAirtable.items import SiteItem, site_config_fields


class UpdatesitesSpider(scrapy.Spider):
    name = "updateSites"
    allowed_domains = ["api.airtable.com"]

    def get_request(self, offset=None):
        req_fields = [
            "id",
            "approved",
            "is_active",
            "name",
            "url",
            "type",
            "article",
            "following",
            "login_url",
            "depth",
            "delay",
            "ua",
            "selenium",
        ]
        url = (
            f"https://api.airtable.com/v0/{self.settings.get('AIRTABLE_BASE_ID')}/Sites?"
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
        fields = record["fields"]
        return SiteItem(
            {
                "airtable_id": fields["id"],
                "approved": fields["approved"],
                "is_active": "is_active" in fields and fields["is_active"],
                "name": fields["name"],
                "url": fields["url"],
                "type": fields["type"],
                "config": {k: fields[k] for k in site_config_fields if k in fields},
                "site_info": {},
            }
        )

    def filter_record(self, site):
        accepted = False
        accepted_site_types = self.settings.get("SITE_TYPES")
        if site["type"] in accepted_site_types:
            accepted = True
        return accepted

    def parse(self, response):
        data = json.loads(response.text)
        for record in data["records"]:
            site = self.parse_record(record)
            accepted = self.filter_record(site)
            if not accepted:
                continue
            if not ("approved" in site and site["approved"]):
                continue
            yield site
        if "offset" in data:
            yield self.get_request(offset=data["offset"])
