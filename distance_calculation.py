import math
from typing import List


from app.extensions import db


class City(db.Model):
    __tablename__
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    latitude = db.Column(db.Decimal(8, 6))
    longitude = db.Column(db.Decimal(9, 6))


    @staticmethod
    def get_column_values():
        data = City.query.with_entities(City.latitude, City.longitude).all()
        return data

    @staticmethod
    def get_unique_city_ids():
        unique_ids = OtherTable.query.with_entities(OtherTable.city_id).distinct().all()
        return [id[0] for id in unique_ids] 

    @staticmethod
    def get_column_values():
        unique_ids = OtherTable.get_unique_city_ids()
        data = City.query.filter(City.id.in_(unique_ids)).with_entities(City.latitude, City.longitude).all()
        return data

class ShortestDistance:
    def __init__(self, lat_curent: float, lng_curent: float) -> None:
        self.lat_curent = lat_curent
        self.lng_curent = lng_curent

    def calculate_destances(self, lat: float, lng: float)-> float:
        return math.sqrt((lat - self.lat_curent) ** 2 + (lng - self.lng_curent) ** 2)

    def find_shortest_distance(self, city_cordinates:List[float]):
        distances = []
        for coord in city_cordinates:
            lat, lng = coord
            distance = self.calculate_destances(lat=lat, lng=lng)
            distances.append(distance)
        return sorted(distances)