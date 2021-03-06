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

    tag, title = get_showtimes(url, date)
    movie = ""
    show_times = ""

    # scrap and match movie name and language then get the showtimes
    for t in tag[0].find_all("div", attrs={"class": "fleft cmain"}):
        for z in t.find_all("span", attrs={"class": "mname"}):
            if config["movie_name"].lower() in z.string.lower():
                if (config["language"].lower() and
                        config["language"].lower() in z.string.lower()):
                    movie = "{0} ".format(z.string)
                    g = t.find_all("a", attrs={"class": "venclick"})
                    for k in g:
                        show_times += "{0} ".format(k.string)

    if show_times:
        # remove unwanted content from cinema hall title
        cinema_hall = title
        return [movie, cinema_hall, show_times]


def get_showtimes(url, date):
    # send a request to the cinema hall url in the city scraped in main()
    res = requests.get(config["base_URL"] + url + "?did=" + date,
                       headers={"User-Agent": config["user_agent"]}
                       )
    soup = BeautifulSoup(res.content, "html.parser")
    tag = soup.find_all(attrs={"class": "noRec"})
    return [tag, soup.title.string[:-55]]


def push_it(pushbullet_obj, device_id, movie_title, movie_showtimes):
    pushbullet_obj.pushNote(device_id, movie_title, movie_showtimes)


def check_config():
    valid = ["city", "movie_name", "language", "month", "day",
             "access_token", "device_nickname"]
    # filter empty config values and end program if any value is empty
    filter_config = dict((k, v) for k, v in config.items() if v and k in valid)
    if len(filter_config) != len(valid):
        return False
    else:
        return True


def pushbullet_magic():
    p = PushBullet(config["access_token"])
    devices = p.getDevices()
    iden = ""
    for dev in devices:
        if ("nickname" in dev.keys() and
                dev["nickname"] == config["device_nickname"]):
            iden = dev["iden"]
            break
    return [p, iden]


def get_cinema_halls():
    # send a request to http://bookmyshow.com/city/cinemas to get all
    # cinema halls in the city
    try:
        res = requests.get(config["base_URL"] + config["city"] + "/cinemas",
                           headers={"User-Agent": config["user_agent"]}
                           )
        soup = BeautifulSoup(res.content, "html.parser")
        tag = soup.find_all("div", attrs={"class": "cinlst"})
        return tag
    except requests.ConnectionError:
        return False


def main():

    # check if config file has all data that is required
    check_data = check_config()
    if check_data:
        tag = get_cinema_halls()
        movie_url = []
        # scrap all cinema hall url's in the city
        if tag:
            for a_href in tag[0].find_all("a"):
                movie_url.append(a_href['href'])

            final_showtimes = ""
            movie_full_title = ""
            # get the showtimes for the movie in the cinema hall from url's
            # scraped
            for url in movie_url:
                details = showtimes(url)
                if details is not None:
                    if not movie_full_title:
                        movie_full_title = "{0}".format(details[0])
                    final_showtimes += "{0}\n".format(details[1])
                    final_showtimes += "    {0}\n".format(details[2])

            final_showtimes = final_showtimes.strip()
            if final_showtimes:
                p, iden = pushbullet_magic()
                if iden:
                    push_it(p, iden, movie_full_title, final_showtimes)
                print(movie_full_title + "\n" + final_showtimes)
            else:
                print("No showtimes found!")
        elif tag is False:
            print("Connection Error!")
        else:
            print("Incorrect city detected! Change the city value in config "
                  "file!")
    else:
        print("Missing data in config file!")


if __name__ == "__main__":
    config = configobj.ConfigObj("config.ini")
    main()
