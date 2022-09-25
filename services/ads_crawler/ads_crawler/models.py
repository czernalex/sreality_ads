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
    price = Column("price", Integer)
    locality = Column("locality", Text())
    img_url = Column("img_url", Text())

    def __init__(self, name, price, locality, img_url):
        self.name = name
        self.price = price
        self.locality = locality
        self.img_url = img_url
