from requests import get

loc = get('https://ipapi.co/8.8.8.8/city/')
print (loc.json())