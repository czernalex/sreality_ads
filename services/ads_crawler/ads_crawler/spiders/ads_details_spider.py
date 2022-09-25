import scrapy
import json

from sqlalchemy.orm import sessionmaker

from ads_crawler.models import Ad, db_connect
from ads_crawler.items import AdsDetailsCrawlerItem


class AdsDetailSpider(scrapy.Spider):
    name = "ads_details"
    custom_settings = {
        "ITEM_PIPELINES": {
            "ads_crawler.pipelines.AdsDetailsCrawlerPipeline": 301
        }
    }

    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def start_requests(self):
        session = self.Session()
        ads = session.query(Ad)
        session.close()
        request_url = "https://sreality.cz/api/cs/v2/estates/{estate_id}"
        for ad in ads:
            yield scrapy.Request(
                url=request_url.format(
                    estate_id=ad.estate_id
                ),
                callback=self.parse,
                meta={
                    "estate_id": ad.estate_id
                }
            )
            # break

    def parse(self, response):
        # with open("./{}.txt".format(response.meta.get("estate_id")), 'w') as f:
        #     f.write(response.text)
        ad_price_data = json.loads(response.text)
        item = AdsDetailsCrawlerItem()
        item["estate_id"] = response.meta.get("estate_id", "estate-id-placeholder")
        item["price"] = ad_price_data.get("price_czk", {}).get("value_raw", 0)
        item["price_str"] = ad_price_data.get("price_czk", {}).get("value", "estate-price-placeholder")
        item["description"] = ad_price_data.get("text",  {}).get("value", "estate-description-placeholder")
        yield item
