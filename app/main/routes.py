from flask import render_template
from app.main import bp
from requests import get
import json
from app.models.city import City
from app.extensions import db





@bp.route("/")
def index():
    response = get("https://httpbin.org/ip")
    r = response.json()
    ip = r["origin"]
    loc = get(f"https://ipapi.co/{r['origin']}/json/")
    city_json = loc.json()
    city = city_json["city"]
    print(city)

    return render_template("index.html", user_location=city, user_ip=ip)
