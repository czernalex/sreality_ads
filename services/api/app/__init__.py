from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("app.config.Config")
app.config["JSON_AS_ASCII"] = False
db = SQLAlchemy(app)


class Ad(db.Model):
    __tablename__ = "ads"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    price = db.Column(db.Integer)
    locality = db.Column(db.Text())
    img_url = db.Column(db.Text())

    def __init__(self, name, price, locality, img_url):
        self.name = name
        self.price = price
        self.locality = locality
        self.img_url = img_url


@app.route("/api")
def get_ads():
    response = {"data": []}
    ads = db.session.query(Ad)
    for ad in ads:
        response["data"].append(
            {
                "id": ad.id,
                "name": ad.name,
                "price": ad.price,
                "locality": ad.locality,
                "img_url": ad.img_url
            }
        )
    return response


@app.route("/ads")
def get_rendered_ads():
    response = """
        <!doctype html>
        <title>sreality ads</title>
        <h1>Sreality ads - flats for sale</h1>
        <ol>
            {ads}
        </ol>
    """
    ads = db.session.query(Ad)
    ads_response = ""
    for ad in ads:
        ads_response += """
            <li>
                <ul>
                    <li>{name}</li>
                    <li>{locality}</li>
                    <li>{price} CZK</li>
                    <li><img src={img_url} alt=sreality.cz style=width:100px;height:100px></li>
                </ul>
            </li>
        """.format(
            name=ad.name,
            locality=ad.locality,
            price=ad.price,
            img_url=ad.img_url
        )
    return response.format(ads=ads_response)
