import json
from flask import render_template
from requests import get
from app.routes import bp
from app.models.models import City, ShortestDistance, ScrapeData
from app import db


@bp.route("/setup")
def setup_city_data():
    scraped_city = ScrapeData(
        title="Wheeeeee",
        start_date="123555-5435-345",
        end_date="234777",
        link="www.ok.lt",
        city_id=2,
        category_id=2,
    )
    db.session.add(scraped_city)
    db.session.commit()

    with open("lt.json", encoding="utf8") as f:
        data = json.load(f)

        for city in data:
            city_title = city["city"]
            print(city_title)
            city_latitude = city["lat"]
            print(city_latitude)
            city_longitude = city["lng"]
            location = City(
                city_name=city_title, latitude=city_latitude, longitude=city_longitude
            )

            db.session.add(location)
            db.session.commit()


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
    ).limit(10)
    distances_with_names = []
    for city_info in city_data:
        city_name, lat, lng = city_info
        distance = distances.calculate_distances(lat, lng)
        distances_with_names.append((city_name, distance))

    distances_with_names.sort(key=lambda x: x[1])
    print(distances_with_names)

    try:
        all_cites = City.query.all()
    except:
        all_cites = []

    return render_template(
        "index.html",
        user_location=city,
        user_ip=ip,
        latitude=latitude,
        longitude=longitude,
        distances_with_names=distances_with_names,
        all_cites=all_cites,
    )
