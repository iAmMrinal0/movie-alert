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
from PushBullet import PushBullet


# validate the PushBullet access token and if valid return device nicknames
def validate(token):
    try:
        p = PushBullet(token)
        devices = p.getDevices()
        nick = [False]
        for dev in devices:
            if "nickname" in dev.keys():
                nick.append(dev["nickname"])
        return nick
    except requests.HTTPError:
        return [True]
    except requests.ConnectionError:
        return ["conn_err"]


def main():
    if not config["city"]:
        city = input("Which city to track the movie in?")
        config["city"] = city

    movie = input("Which movie to track? ")
    config["movie_name"] = movie

    language = input("Which language should the movie be tracked in? ")
    config["language"] = language

    day = input("What date(dd) do you want to track it? ")
    config["day"] = day if len(day) == 2 else "0" + day

    if not config["month"]:
        month = input("Which month(mm) should the movie be tracked in? ")
        config["month"] = month

    nickname_list = []
    conn_err = False
    if not config["access_token"]:
        check = True
        while check:
            access_token = input("Enter access token: ")
            check_nick = validate(access_token)
            check = check_nick[0]
            if not check and not check == "conn_err":
                config["access_token"] = access_token
                if len(check_nick) > 1:
                    nickname_list = check_nick[1:]
            if check == "conn_err":
                conn_err = True
                break

    # use nickname_list to get name of device to send notification to
    if not config["device_nickname"] and nickname_list:
        for i in range(0, len(nickname_list)):
            print("{0}. {1}".format(i + 1, nickname_list[i]))
        while True:
            nickname = input("Which device(1,{0}) would you like the "
                             "notification sent to?".format(i + 1))
            if int(nickname) in range(1, i + 2):
                config["device_nickname"] = nickname_list[
                    int(nickname) - 1]
                break
    config.write()  # save all config values in config.ini
    if not conn_err:
        print("'{0}' on {1}-{2}-{3} will be tracked and will be sent to '{4}'".
              format(config["movie_name"], config["day"], config["month"],
                     config["year"], config["device_nickname"])
              )
    else:
        print("Connection error!")

if __name__ == "__main__":
    config = configobj.ConfigObj("config.ini")
    main()
