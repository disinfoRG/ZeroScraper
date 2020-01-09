import scrapy

## this needs not be a scrapy item but just a data object
class SiteConfig(scrapy.Item):
    article = scrapy.Field()
    following = scrapy.Field()
    depth = scrapy.Field()
    delay = scrapy.Field()
    ua = scrapy.Field()
    selenium = scrapy.Field()

    def update(self, d):
        return super(scrapy.Item, self).update(
            {
                k: d[k]
                for k in ["article", "following", "depth", "delay", "ua", "selenium"]
                if k in d and d[k] is not None
            }
        )

    @staticmethod
    def default():
        return SiteConfig(
            {
                "depth": 5,
                "delay": 1.5,
                "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                "following": "",
                "selenium": False,
            }
        )
