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

import configobj
import requests
from bs4 import BeautifulSoup
from PushBullet import PushBullet


def get_movie_url():
    # request in.bookmyshow.com/{city_name}/movies to get URL of required movie
    url = config["base_URL"] + config["city"] + "/movies"
    try:
        req = requests.get(url, headers={"User-Agent": config["user_agent"]})
        source = BeautifulSoup(req.content, "html.parser")
        tags = source.find_all("section",
                               attrs={"class": "language-based-formats"})

        for tag in tags:
            c = tag.find_all("a")
            h = tag.find_all("h2")
            m_name = config["movie_name"].lower().replace(" ", "-")
            if (config['language'].lower() == h[0].text.lower() and
                    m_name in c[0]["href"]):
                return c[0]['href'][1:-9]
    except requests.ConnectionError:
        return False


def get_show_times(url):
    # get show times based on previous URL with the year+month+day concatenated
    show_url = "{0}{1}{2}{3}{4}".format(config["base_URL"], url,
                                        config["year"], config["month"],
                                        config["day"])
    try:
        req = requests.get(show_url,
                           headers={"User-Agent": config["user_agent"]})
        source = BeautifulSoup(req.content, "html.parser")
        m_name = source.find("h1", attrs={"itemprop": "name"})
        if m_name:
            movie_name = m_name["content"]
            cinema_halls = source.find_all("div", attrs={"class": "container"})
            result = dict()
            for cin in cinema_halls:
                halls = cin.find_all("li", attrs={"class": "list"})
                for temp in halls:
                    if temp["data-is-down"] == "false":
                        times = temp.find_all("div",
                                              attrs={"data-online": "Y"})
                        if times:
                            result.setdefault(temp["data-name"], [])
                            for im in times:
                                result[temp["data-name"]].append(
                                    im.text.strip()
                                )
            return [movie_name, result]
        else:
            return False
    except requests.ConnectionError:
        return False


def push_it(data):
    # push the movie name and cinema hall with movie timings to selected
    # pushbullet device
    movie_name = data[0]
    show_times = data_to_string(data[1])
    iden = config["device_iden"]
    if iden:
        try:
            p.pushNote(iden, movie_name, show_times)
            return [True, movie_name, show_times]
        except requests.ConnectionError:
            return [False]
    else:
        return [None]


def data_to_string(data):
    # cinema halls and show times is a dictionary with list values
    result = ""
    for key, value in data.items():
        times = " ".join(value)
        result += "{0}\n{1}\n\n".format(key, times)
    return result


def check_config():
    # check if none of the values in config.ini are empty
    valid = ["city", "movie_name", "language", "month", "day",
             "access_token", "device_iden", "device_nickname"]
    # filter empty config values and end program if any value is empty
    filter_config = dict((k, v) for k, v in config.items() if v and k in valid)
    if len(filter_config) != len(valid):
        return False
    else:
        return True


def main():
    if check_config():
        url = get_movie_url()
        result = get_show_times(url)
        if result:
            pushed = push_it(result)
            if pushed[0] is None:
                print("No matching devices found!")
            elif pushed[0]:
                print("{0}\n{1}".format(pushed[1], pushed[2]))
            else:
                print("Connection error!")
    else:
        print("Check config.ini for incorrect/missing values!")


if __name__ == "__main__":
    config = configobj.ConfigObj("config.ini")
    p = PushBullet(config["access_token"])
    main()
