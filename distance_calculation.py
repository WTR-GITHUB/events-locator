import math
from typing import List


from app.extensions import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    latitude = db.Column(db.Decimal(8, 6))
    longitude = db.Column(db.Decimal(9, 6))


    def get_column_values():
        data = query(City.latitude, City.longitude).all()
        return data

class ShortestDistance:
    def __init__(self, lat_curent: float, lng_curent: float) -> None:
        self.lat_curent = lat_curent
        self.lng_curent = lng_curent

    def calculate_destances(self, lat: float, lng: float)-> float:
        return math.sqrt((lat - self.lat_curent) ** 2 + (lng - self.lng_curent) ** 2)

    def find_shortest_distance(self, city_cordinates:List[float]):


    def get_column_values():
        data = City.query.with_entities(City.latitude, City.longitude).all()
        return data