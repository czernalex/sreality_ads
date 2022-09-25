from sqlalchemy.orm import sessionmaker

from .models import Ad, db_connect, db_create_table, db_drop_table


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
            item["price"],
            item["locality"],
            item["img_url"]
        )
        session.add(ad)
        session.commit()
        session.close()
        return item
