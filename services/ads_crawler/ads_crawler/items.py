from asyncio import SubprocessTransport
import scrapy


class AdsCrawlerItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    locality = scrapy.Field()
    img_url = scrapy.Field()
