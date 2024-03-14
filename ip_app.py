from requests import get

loc = get('https://ipapi.co/193.219.65.21/city/')
print (loc.text)

# from requests import get

# loc = get('https://ipapi.co/8.8.8.8/json/')
# print (loc.json())

# import subprocess

# result = subprocess.run(["curl", "-s", "https://ipapi.co/193.219.65.21/city/"], stdout=subprocess.PIPE)
# print(result.stdout)