import math
from app.extensions import db
from typing import List



class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(40))
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
    

class Category(db.Model):
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
    city = db.relationship("City", cascade="all, delete", passive_deletes=True)
    category_id = db.Column(db.Integer, db.ForeignKey("catogory.id"))
    category = db.relationship("Category", cascade="all, delete", passive_deletes=True)


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
    
# Cia ateina musu dabartine coordinate pasiimame is tos funkcijos
distances = ShortestDistance(23, 53)


city_data = City.query.with_entities(City.city_name, City.latitude, City.longitude).all()
distances_with_names = []
for city_info in city_data:
    city_name, lat, lng = city_info
    distance = distances.calculate_distance(lat, lng)
    distances_with_names.append((city_name, distance))

distances_with_names.sort(key=lambda x: x[1])

for city_name, distance in distances_with_names:
    print(f"{city_name}: {distance}")

# žžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžžž


unique_city_ids = ScrapeData.query.with_entities(ScrapeData.city_id).distinct().all()


city_names_by_id = {}
for city_id, in unique_city_ids:
    city = City.query.filter_by(id=city_id).first()
    if city:
        city_names_by_id[city_id] = city.city_name

# Calculate distances and store them along with city names
distances_with_names = []
for city_info in city_data:
    city_id, lat, lng = city_info
    if city_id in city_names_by_id:
        city_name = city_names_by_id[city_id]
        distance = distances.calculate_distance(lat, lng)
        distances_with_names.append((city_name, distance))

# Sort distances based on distance
distances_with_names.sort(key=lambda x: x[1])

# Print city name and distance
for city_name, distance in distances_with_names:
    print(f"{city_name}: {distance}")