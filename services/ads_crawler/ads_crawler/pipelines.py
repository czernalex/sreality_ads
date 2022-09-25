from sqlalchemy.orm import sessionmaker

from .models import Ad, AdDetail, db_connect, db_create_table, db_drop_table


class AdsCrawlerPipeline:
    def __init__(self):
        engine = db_connect()
        db_drop_table(engine)
        db_create_table(engine)
        self.Session = sessionmaker(bind=engine)
    
    def process_item(self, item, spider):
        session = self.Session()
        ad = Ad(
            item["name"],
            item["estate_id"],
            item["locality"],
            item["img_url_1"],
            item["img_url_2"],
            item["img_url_3"]
        )
        session.add(ad)
        session.commit()
        session.close()
        return item


class AdsDetailsCrawlerPipeline:
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        ad_price = AdDetail(
            item["estate_id"],
            item["price"],
            item["price_str"],
            item["description"]
        )
        session.add(ad_price)
        session.commit()
        session.close()
        return item
