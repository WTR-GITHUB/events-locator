from flask import render_template
from app.main import bp
from requests import get
import json
from app.models.city import City
from app.extensions import db

# from app.models.models import ShortestDistance


@bp.route("/")
def index():
    response = get("https://httpbin.org/ip")
    r = response.json()
    ip = r["origin"]
    loc = get(f"https://ipapi.co/{r['origin']}/json/")
    city_json = loc.json()
    city = city_json["city"]
    print(city)
    latitude = city_json["latitude"]
    longitude = city_json["longitude"]

    distances = ShortestDistance(lat_curent=latitude, lng_curent=longitude)

    city_data = City.query.with_entities(
        City.city_name, City.latitude, City.longitude
    ).all()
    distances_with_names = []
    for city_info in city_data:
        city_name, lat, lng = city_info
        distance = distances.calculate_distance(lat, lng)
        distances_with_names.append((city_name, distance))

    distances_with_names.sort(key=lambda x: x[1])

    return render_template(
        "index.html",
        user_location=city,
        user_ip=ip,
        latitude=latitude,
        longitude=longitude,
    )
