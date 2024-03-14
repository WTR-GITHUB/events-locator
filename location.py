from requests import get

response = get('https://httpbin.org/ip')
r = response.json()

loc = get(f"https://ipapi.co/{r['origin']}/city/")
location = loc.json()