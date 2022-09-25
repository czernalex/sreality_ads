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
    estate_id = db.Column(db.Text())
    locality = db.Column(db.Text())
    img_url_1 = db.Column(db.Text())
    img_url_2 = db.Column(db.Text())
    img_url_3 = db.Column(db.Text())

    def __init__(self, name, estate_id, locality, img_url_1, img_url_2, img_url_3):
        self.name = name
        self.estate_id = estate_id
        self.locality = locality
        self.img_url_1 = img_url_1
        self.img_url_2 = img_url_2
        self.img_url_3 = img_url_3


class AdDetail(db.Model):
    __tablename__ = "ads_details"

    id = db.Column(db.Integer, primary_key=True)
    estate_id = db.Column(db.Text())
    price = db.Column(db.Integer)
    price_str = db.Column(db.Text())
    description = db.Column(db.Text())

    def __init__(self, estate_id, price, price_str, description):
        self.estate_id = estate_id
        self.price = price
        self.price_str = price_str
        self.description = description


@app.route("/api")
def get_ads():
    response = {"data": []}
    ads = db.session.query(Ad)
    for ad in ads:
        ad_detail = db.session.query(AdDetail).filter_by(estate_id=ad.estate_id).first()
        ad_detail_response = {}
        if ad_detail is not None:
            ad_detail_response["price_raw"] = ad_detail.price_str
            ad_detail_response["price"] = ad_detail.price
            ad_detail_response["description"] = ad_detail.description
        response["data"].append(
            {
                "id": ad.id,
                "name": ad.name,
                "estate_id": ad.estate_id,
                "locality": ad.locality,
                "img_url_1": ad.img_url_1,
                "img_url_2": ad.img_url_2,
                "img_url_3": ad.img_url_3,
                "ad_detail": ad_detail_response
            }
        )
    return response


@app.route("/")
def get_rendered_ads():
    response = """
        <!doctype html>
        <title>Sreality ads</title>
        <h1>Sreality ads - flats for sale</h1>
        <div style=width:800px;>
            <ol>
                {ads}
            </ol>
        </div>
    """
    ads = db.session.query(Ad)
    ads_response = ""
    for ad in ads:
        ad_detail = db.session.query(AdDetail).filter_by(estate_id=ad.estate_id).first()
        ads_response += """
            <li>
                <ul>
                    <li>{name}</li>
                    <li>{locality}</li>
                    <li>{price_str} CZK</li>
                    <li><p>{description}</p></li>
                </ul>
                <div style=display:flex;>
                    <div style=flex:33.33%;padding:5px;>
                        <img src={img_url_1} alt=img1_sreality.cz style=width:200px;height:200px> 
                    </div>
                    <div style=flex:33.33%;padding:5px;>
                        <img src={img_url_2} alt=img2_sreality.cz style=width:200px;height:200px> 
                    </div>
                    <div style=flex:33.33%;padding:5px;>
                        <img src={img_url_3} alt=img3_sreality.cz style=width:200px;height:200px> 
                    </div>
                </div>
                <hr>
            </li>
        """.format(
            name=ad.name,
            locality=ad.locality,
            price_str=ad_detail.price_str if ad_detail is not None else "price-placeholder",
            description=ad_detail.description if ad_detail is not None else "description-placeholder",
            img_url_1=ad.img_url_1,
            img_url_2=ad.img_url_2,
            img_url_3=ad.img_url_3
        )
    return response.format(ads=ads_response)
