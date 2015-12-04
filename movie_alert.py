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
    url = config["base_URL"] + config["city"] + "/movies"
    try:
        req = requests.get(url, headers={"User-Agent": config["user_agent"]})
        source = BeautifulSoup(req.content, "html.parser")
        tags = source.find_all("section",
                               attrs={"class": "language-based-formats"})

        for tag in tags:
            c = tag.find_all("a")
            h = tag.find_all("h2")
            if (config['language'].lower() == h[0].text.lower() and
                    config["movie_name"].lower() in c[0]["href"]):
                return c[0]['href'][1:-9]
    except requests.ConnectionError:
        return False


def get_show_times(url):
    show_url = "{0}{1}{2}{3}{4}".format(config["base_URL"], url,
                                        config["year"], config["month"],
                                        config["day"])
    try:
        req = requests.get(show_url,
                           headers={"User-Agent": config["user_agent"]})
        source = BeautifulSoup(req.content, "html.parser")
        m_name = source.find("h1", attrs={"itemprop": "name"})
        movie_name= m_name["content"]
        cinema_halls = source.find_all("div", attrs={"class": "container"})
        result = dict()
        for cin in cinema_halls:
            halls = cin.find_all("li", attrs={"class": "list"})
            for temp in halls:
                if temp["data-is-down"] == "false":
                    times = temp.find_all("div", attrs={"data-online": "Y"})
                    if times:
                        result.setdefault(temp["data-name"], [])
                        for im in times:
                            result[temp["data-name"]].append(im.text.strip())
        return [movie_name, result]
    except requests.ConnectionError:
        return False


def push_it(data):
    devices = p.getDevices()
    iden = ""
    movie_name = data[0]
    show_times = data_to_string(data[1])
    for dev in devices:
        if ("nickname" in dev.keys() and
                dev["nickname"] == config["device_nickname"]):
            iden = dev["iden"]
            break
    if iden:
        p.pushNote(iden, movie_name, show_times)


def data_to_string(data):
    result = ""
    for key, value in data.items():
        times = " ".join(value)
        result += "{0}\n{1}\n\n".format(key, times)
    return result


def main():
    url = get_movie_url()
    result = get_show_times(url)
    push_it(result)


if __name__ == "__main__":
    config = configobj.ConfigObj("config.ini")
    p = PushBullet(config["access_token"])
    main()
