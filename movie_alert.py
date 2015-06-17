import requests
from bs4 import BeautifulSoup

from PushBullet import PushBullet


# Movie details: partial/complete movie name in lowercase, language in lowercase, date
movie_name = "jurassic"
language = "english"
year = "2015"
month = "06"
day = "18"
date = year + month + day

# Bookmyshow URL for the specific movie hall.
bookmyshow_URL = ""

# PushBullet Access Token
access_token = ""

heads = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"}

results = requests.get(bookmyshow_URL + date, headers=heads)

soup = BeautifulSoup(results.content)

tag = soup.find_all(attrs={"class": "noRec"})

movie = ""
show_times = ""

# Device index as per listing on PushBullet.com
# Here 0 is the first device in the list. Change as required.
device_index = 0

for t in tag[0].find_all("div", attrs={"class": "fleft cmain"}):
    for z in t.find_all("span", attrs={"class": "mname"}):
        if movie_name in z.string.lower() and language in z.string.lower():
            movie = "{} ".format(z.string)
            g = t.find_all("a", attrs={"class": "venclick"})
            for k in g:
                show_times += "{} ".format(k.string)

if movie and show_times:
    p = PushBullet(access_token)
    devices = p.getDevices()  # Get list of devices registered for the account on PushBullet
    p.pushNote(devices[device_index]["iden"], movie, show_times)
    print(movie + show_times)
else:
    print("No movie showtimes found!")
