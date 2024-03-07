from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import requests


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)

class Test(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    date = db.Column(db.String(200))
    city = db.Column(db.String(200))
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)
    sunrise_hour = db.Column(db.String(100))
    sunset_hour = db.Column(db.String(100))

    with app.app_context():
        db.create_all()




@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/", methods=['POST'])
def city():
    weather_status = []
    day = []
    currentCity = request.form.get("city")
    processedCity = currentCity.lower().capitalize()
    days = 3
    api_url = "http://api.weatherapi.com/v1/forecast.json"
    api_key = "ee0eefcce1334187937122206240703"
    params = {"key": api_key, "q": processedCity, "days": days}
    response = requests.post(api_url, params=params)
    if response:
        response_json = response.json()
        for i in range(days):
            weather_status.append(response_json["forecast"]["forecastday"][i]["day"]["condition"]["text"])
            day.append(response_json["forecast"]["forecastday"][i]["date"])
        
        try:
            entry = Test(
                    date = response_json["forecast"]["forecastday"][0]["date"],
                    city= response_json["location"]["name"],
                    max_temp = response_json["forecast"]["forecastday"][0]["day"]["maxtemp_c"],
                    min_temp= response_json["forecast"]["forecastday"][0]["day"]["mintemp_c"],
                    total_precipitation = response_json["forecast"]["forecastday"][0]["day"]["totalprecip_mm"],
                    sunrise_hour = response_json["forecast"]["forecastday"][0]["astro"]["sunrise"],
                    sunset_hour = response_json["forecast"]["forecastday"][0]["astro"]["sunset"],
            )
            db.session.add(entry)
            db.session.commit()
        except:
            print("An exception has occurred")
        return render_template("index.html", weather_status = weather_status, day = day)
    else:
        return render_template("index.html")

def index():
    return render_template('index.html')


if __name__ == "__main__":
  
    app.run(debug=True)