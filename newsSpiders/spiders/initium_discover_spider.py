import os
from scrapy.http import FormRequest, Request

from newsSpiders.spiders.basic_discover_spider import BasicDiscoverSpider


class LoginError(Exception):
    pass


class InitiumDiscoverSpider(BasicDiscoverSpider):
    name = "initum_discover"

    def __init__(self, login_url, credential_tag, **kwargs, ):
        super().__init__(**kwargs)
        self.login_url = login_url
        self.credentials = {
            "email": os.getenv(f"{credential_tag.upper()}_EMAIL"),
            "password": os.getenv(f"{credential_tag.upper()}_PWD")
        }

    def start_requests(self):
        yield FormRequest(url=self.login_url,
                          headers={"X-Client-Name": "Web",
                                   "User-Agent": "Mozilla/5.0",
                                   "Authorization": "Basic YW5vbnltb3VzOkdpQ2VMRWp4bnFCY1ZwbnA2Y0xzVXZKaWV2dlJRY0FYTHY="},
                          formdata=self.credentials,
                          callback=self.check_login_response,
                          dont_filter=True)

    def check_login_response(self, response):
        if self.credentials["email"] in response.body.decode("utf-8"):
            self.logger.info("Login successfully.")
            return Request(self.site_url)
        else:
            raise LoginError("Login failed.")
