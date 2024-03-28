import json
from flask import render_template, jsonify
from requests import get
from app.routes import bp
from app.models.models import City, ShortestDistance, ScrapeData
from app import db
from app import scrape_and_update


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

    # scrape_and_update()
    with open("lt.json", encoding="utf8") as f:
        data = json.load(f)
        for city in data:
            city_title = city["city"]
            print(city_title)
            city_latitude = city["lat"]
            print(city_latitude)
            city_longitude = city["lng"]
            location = City(
                city_name=city_title,
                latitude=city_latitude,
                longitude=city_longitude,
            )
            db.session.add(location)
            db.session.commit()
    return render_template("setup_success.html")
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500


@bp.route("/")
def index():
    try:
        response = get("https://httpbin.org/ip")
        r = response.json()
        ip = r["origin"]

        loc = get(f"https://ipapi.co/{r['origin']}/json/")
        city_json = loc.json()
        city = city_json.get("city", "Kaunas")  # Get city or use "Kaunas" as default
        latitude = city_json.get(
            "latitude", 54.9038
        )  # Get latitude or use default value
        longitude = city_json.get(
            "longitude", 23.8924
        )  # Get longitude or use default value

    except KeyError as e:
        print(f"KeyError occurred: {e}")
        city = "Kaunas"
        latitude = 54.9038
        longitude = 23.8924

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
        all_cities = City.query.all()
    except:
        all_cities = []

    return render_template(
        "index.html",
        user_location=city,
        user_ip=ip,
        latitude=latitude,
        longitude=longitude,
        distances_with_names=distances_with_names,
        all_cities=all_cities,
    )
