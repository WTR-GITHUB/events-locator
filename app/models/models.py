import math
from typing import List
from app import db


class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(40))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    @staticmethod
    def get_unique_city_ids():
        unique_ids = City.query.with_entities(City.city_id).distinct().all()
        return [id[0] for id in unique_ids]

    @staticmethod
    def get_column_values():
        unique_ids = City.get_unique_city_ids()
        data = (
            City.query.filter(City.id.in_(unique_ids))
            .with_entities(City.latitude, City.longitude)
            .all()
        )
        return data


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))


class ScrapeData(db.Model):
    __tablename__ = "scrape_data"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    start_date = db.Column(db.String(12))
    end_date = db.Column(db.String(12))
    link = db.Column(db.String(100))
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    city = db.relationship("City")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category")


class ShortestDistance:
    CONSTANT = 111.32 # This is a constant to convert latitude and logitude to km
    def __init__(self, lat_curent: float, lng_curent: float) -> None:
        self.lat_curent = lat_curent
        self.lng_curent = lng_curent

    def calculate_distances(self, lat: float, lng: float) -> float:
        return round(
            math.sqrt(
                (float(lat) * self.CONSTANT - self.lat_curent * self.CONSTANT) ** 2
                + (float(lng) * self.CONSTANT - self.lng_curent * self.CONSTANT) ** 2
            ),
            2,
        )

    def find_shortest_distance(self, city_cordinates: List[float]):
        distances = []
        for coord in city_cordinates:
            lat, lng = coord
            distance = self.calculate_distances(lat=lat, lng=lng)
            distances.append(distance)
        return sorted(distances)
