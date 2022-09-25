import os

from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def db_connect():
    return create_engine(
        os.getenv("DATABASE_URL", "sqlite://")
    )


def db_drop_table(engine):
    Base.metadata.drop_all(bind=engine)


def db_create_table(engine):
    Base.metadata.create_all(bind=engine)


class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    name = Column("name", Text())
    estate_id = Column("estate_id", Text())
    locality = Column("locality", Text())
    img_url_1 = Column("img_url_1", Text())
    img_url_2 = Column("img_url_2", Text())
    img_url_3 = Column("img_url_3", Text())

    def __init__(self, name, estate_id, locality, img_url_1, img_url_2, img_url_3):
        self.name = name
        self.estate_id = estate_id
        self.locality = locality
        self.img_url_1 = img_url_1
        self.img_url_2 = img_url_2
        self.img_url_3 = img_url_3


class AdDetail(Base):
    __tablename__ = "ads_details"

    id = Column(Integer, primary_key = True)
    estate_id = Column("estate_id", Text())
    price = Column("price", Integer)
    price_str = Column("price_str", Text())
    description = Column("description", Text())

    def __init__(self, estate_id, price, price_str, description):
        self.estate_id = estate_id
        self.price = price
        self.price_str = price_str
        self.description = description
