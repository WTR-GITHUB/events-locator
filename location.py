from requests import get

response = get('https://httpbin.org/ip')
r = response.json()

loc = get(f"https://ipapi.co/{r['origin']}/json/")
print (loc.json())
location_data = loc.json()
city = location_data["city"]
latitude = location_data["latitude"]
longitude = location_data["longitude"]