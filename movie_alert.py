# -*- coding: utf-8 -*-
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import configobj
from bs4 import BeautifulSoup
from PushBullet import PushBullet


def showtimes(url):
    date = config["year"] + config["month"] + config["day"]

    res = requests.get(config["base_URL"] + url + "?did=" + date,
                       headers={"User-Agent": config["user_agent"]}
                       )
    soup = BeautifulSoup(res.content)
    tag = soup.find_all(attrs={"class": "noRec"})

    movie = ""
    show_times = ""

    for t in tag[0].find_all("div", attrs={"class": "fleft cmain"}):
        for z in t.find_all("span", attrs={"class": "mname"}):
            if config["movie_name"].lower() in z.string.lower():
                if (config["language"].lower() and
                        config["language"].lower() in z.string.lower()):
                    movie = "{0} ".format(z.string)
                    g = t.find_all("a", attrs={"class": "venclick"})
                    for k in g:
                        show_times += "{0} ".format(k.string)

    if show_times != "":
        cinema_hall = soup.title.string[:-55]
        return [cinema_hall, movie, show_times]


def main():

    res = requests.get(config["base_URL"] + config["city"] +
                       "/cinemas", headers={"User-Agent": config["user_agent"]}
                       )
    soup = BeautifulSoup(res.content)
    tag = soup.find_all("div", attrs={"class": "cinlst"})

    movie_url = []
    if tag:
        for a_href in tag[0].find_all("a"):
            movie_url.append(a_href['href'])

        final_showtimes = ""
        for url in movie_url:
            details = showtimes(url)
            if details is not None:
                final_showtimes += "{0}\n".format(details[0])
                final_showtimes += "    {0}\n".format(details[1])
                final_showtimes += "    {0}\n".format(details[2])

        final_showtimes = final_showtimes.strip()
        if final_showtimes:
            p = PushBullet(config["access_token"])
            devices = p.getDevices()
            iden = ""
            for dev in devices:
                if ("nickname" in dev.keys() and
                        dev["nickname"] == config["device_nickname"]):
                    iden = dev["iden"]
                    break

            if iden:
                p.pushNote(iden, config["movie_name"].title(), final_showtimes)
            print(final_showtimes)
        else:
            print("No showtimes found!")
    else:
        print("Incorrect city detected! Change the city value in config file!")

if __name__ == "__main__":
    config = configobj.ConfigObj("config.ini")
    main()
