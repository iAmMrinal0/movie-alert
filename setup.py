import configobj
import requests
from PushBullet import PushBullet


def validate(token, nick=None):
    if nickname is None:
        try:
            p = PushBullet(token)
            devices = p.getDevices()
            return False
        except requests.exceptions.HTTPError:
            return True
    else:
        p = PushBullet(token)
        devices = p.getDevices()
        for dev in devices:
            if "nickname" in dev.keys() and dev["nickname"] == nick.lower():
                return False
        return True


def main():
    if not config["city"]:
        city = input("Which city to track the movie in?")
        config["city"] = city

    movie = input("Which movie to track? ")
    config["movie_name"] = movie
    day = input("What date(dd) do you want to track it? ")
    config["day"] = day if len(day) == 2 else "0" + day

    if not config["month"]:
        month = input("Which month(mm) should the movie be tracked in? ")
        config["month"] = month

    check = True
    while(check):
        if not config["access_token"]:
            access_token = input("Enter access token: ")
            check = validate(access_token)
            if not check:
                config["access_token"] = access_token

    check = True
    while(check):
        if not config["device_nickname"]:
            nickname = input("Nickname of device to send notification? ")
            check = validate(access_token, nickname)
            if not check:
                config["device_nickname"] = nickname

    config.write()

    print("'{0}' on {1}-{2}-{3} will be tracked and will be sent to '{4}'".
          format(config["movie_name"], config["day"],
                 config["month"], config["year"], config["device_nickname"])
          )

if __name__ == "__main__":
    config = configobj.ConfigObj("config.ini")
    main()
