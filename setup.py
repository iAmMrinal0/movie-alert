import configobj


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

    if not config["access_token"]:
        access_token = input(
            "Enter access token from https://pushbullet.com/#settings: ")
        config["access_token"] = access_token

    if not config["device_nickname"]:
        nickname = input("Nickname of device to send notification?")
        config["device_nickname"] = nickname
    config.write()

    print("'{0}' on {1}-{2}-{3} will be tracked and will be sent to '{4}'".
          format(config["movie_name"], config["day"],
                 config["month"], config["year"], config["device_nickname"])
          )

if __name__ == "__main__":
    config = configobj.ConfigObj("config.ini")
    main()
