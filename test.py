import math
from typing import List
from app.extensions import db

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    latitude = db.Column(db.DECIMAL(8, 6))
    longitude = db.Column(db.DECIMAL(9, 6))

    @staticmethod
    def get_unique_city_ids():
        unique_ids = OtherTable.query.with_entities(OtherTable.city_id).distinct().all()
        return [id[0] for id in unique_ids]

    @staticmethod
    def get_column_values():
        unique_ids = City.get_unique_city_ids()
        data = City.query.filter(City.id.in_(unique_ids)).with_entities(City.latitude, City.longitude).all()
        return data

class ShortestDistance:
    def __init__(self, lat_current: float, lng_current: float) -> None:
        self.lat_current = lat_current
        self.lng_current = lng_current

    def calculate_distance(self, lat: float, lng: float) -> float:
        return math.sqrt((lat - self.lat_current) ** 2 + (lng - self.lng_current) ** 2)

    def find_shortest_distance(self, city_coordinates: List[float]) -> float:
        distances = []
        for coord in city_coordinates:
            lat, lng = coord
            distance = self.calculate_distance(lat=lat, lng=lng)
            distances.append(distance)
        return min(distances)
