from flask import render_template
from app.cities import bp
from app.extensions import db
import json
from app.models.city import City

# with open("lt.json", encoding="utf8") as f:
#         data = json.load(f)

#     for city in data:
#         city_title = city["city"]
#         print(city_title)
#         city_latitude = city["lat"]
#         print(city_latitude)
#         city_longitude = city["lng"]
#         location = City(
#             title=city_title, latitude=city_latitude, longitude=city_longitude
#         )
#         db.session.add(location)
#
#         print(location.latitude)
#         print("--")
#         db.session.commit()


@bp.route("/")
def index():
    try:
        all_cities = City.query.all()
    except:
        all_cities = []

    return render_template("cities/index.html", all_cities=all_cities)


# @bp.route('/categories/')
# def categories():
#     return render_template('posts/categories.html')
