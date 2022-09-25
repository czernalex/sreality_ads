import scrapy
import datetime
import json

from ads_crawler.items import AdsCrawlerItem


class AdsSpider(scrapy.Spider):
    name = "ads"

    def start_requests(self):
        request_url = "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page={page_id}&per_page=20&tms={timestamp}"
        timestamp = int(datetime.datetime.now().timestamp())
        for page_id in range(1):
            yield scrapy.Request(
                url=request_url.format(
                    page_id=page_id+1,
                    timestamp=timestamp
                ),
                callback=self.parse
            )

    def parse(self, response):
        ads_data = json.loads(response.text).get("_embedded", {}).get("estates", [])
        item = AdsCrawlerItem()
        for ad in ads_data:
            item["name"] = ad.get("name", "ad-name-placeholder")
            item["price"] = ad.get("price", 0)
            item["locality"] = ad.get("locality", "ad-locality-placeholder")
            for i in range(3):
                try:
                    item["img_url_{}".format(i+1)] = ad.get("_links", {}).get("images", [])[i].get("href", "ad-img-url-{}-placeholder".format(i+1))
                except IndexError:
                    item["img_url_{}".format(i+1)] = "ad-img-url-{}-placeholder".format(i+1)
            yield item
