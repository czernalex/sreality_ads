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
    img_url_1 = db.Column(db.Text())
    img_url_2 = db.Column(db.Text())
    img_url_3 = db.Column(db.Text())

    def __init__(self, name, price, locality, img_url_1, img_url_2, img_url_3):
        self.name = name
        self.price = price
        self.locality = locality
        self.img_url_1 = img_url_1
        self.img_url_2 = img_url_2
        self.img_url_3 = img_url_3


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
                "img_url_1": ad.img_url_1,
                "img_url_2": ad.img_url_2,
                "img_url_3": ad.img_url_3
            }
        )
    return response


@app.route("/ads")
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
        ads_response += """
            <li>
                <ul>
                    <li>{name}</li>
                    <li>{locality}</li>
                    <li>{price}</li>
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
            price=str(ad.price) + " CZK" if ad.price > 0 else "Info o ceně u RK",
            img_url_1=ad.img_url_1,
            img_url_2=ad.img_url_2,
            img_url_3=ad.img_url_3
        )
    return response.format(ads=ads_response)
