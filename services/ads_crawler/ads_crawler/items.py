import scrapy


class AdsCrawlerItem(scrapy.Item):
    name = scrapy.Field()
    estate_id = scrapy.Field()
    locality = scrapy.Field()
    img_url_1 = scrapy.Field()
    img_url_2 = scrapy.Field()
    img_url_3 = scrapy.Field()


class AdsDetailsCrawlerItem(scrapy.Item):
    estate_id = scrapy.Field()
    price = scrapy.Field()
    price_str = scrapy.Field()
    description = scrapy.Field()
