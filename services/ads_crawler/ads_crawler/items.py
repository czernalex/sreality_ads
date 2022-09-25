from asyncio import SubprocessTransport
import scrapy


class AdsCrawlerItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    locality = scrapy.Field()
    img_url_1 = scrapy.Field()
    img_url_2 = scrapy.Field()
    img_url_3 = scrapy.Field()
