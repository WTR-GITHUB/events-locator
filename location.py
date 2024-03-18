from requests import get

def get_location():
    response = get("https://httpbin.org/ip")
    r = response.json()
    # print(r["origin"])

    loc = get(f"https://ipapi.co/{r['origin']}/json/")  # 193.219.65.21
    # print(loc.json())
    location_data = loc.json()
    city = location_data["city"]
    latitude = location_data["latitude"]
    longitude = location_data["longitude"]

    print(city)
    print(latitude)
    print(longitude)

    return city, latitude, longitude