from scrapy.http import FormRequest, Request
from newsSpiders.spiders.basic_discover_spider import BasicDiscoverSpider
import os


class LogInDiscoverSpider(BasicDiscoverSpider):
    name = "login_discover"

    def __init__(self, login_url, credential_tag, **kwargs,):
        super().__init__(**kwargs)
        self.login_url = login_url
        self.credentials = {
            "email": os.getenv(f"{credential_tag.upper()}_EMAIL"),
            "password": os.getenv(f"{credential_tag.upper()}_PWD")
        }

    def start_requests(self):
        yield Request(url=self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        return FormRequest.from_response(response, formdata=self.credentials, callback=self.check_login_response)

    def check_login_response(self, response):
        if self.credentials["email"] in response.body.decode("utf-8"):
            self.logger.info("Log in successfully!")
            return Request(self.site_url)
        else:
            self.logger.info("Log in failed.")
            raise Exception('LogInError')
