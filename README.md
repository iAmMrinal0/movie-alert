# Movie Alert
A script written in Python to send a PushBullet notification when a particular movie hits the movie hall in your city which is listed on Bookmyshow.

## Requirements
1. Install [Python 3.4](https://www.python.org/download/releases/3.4.3/)  
2. Install requests, beautifulsoup4, websocket-client, configobj using pip.

  - requests - `pip install requests`
  - beautifulsoup4 - `pip install beautifulsoup4`
  - websocket-client - `pip install websocket-client`  
  - configobj - `pip install configobj`

3. Collect your PushBullet access token from [here](https://www.pushbullet.com/#settings/account) and device nickname from [here](https://www.pushbullet.com/#devices)



## Usage
Setup using `python setup.py` and enter your city, movie name, date and month to track, PushBullet access token and device nickname.

Now run `python movie_alert.py` and if a movie is playing on the date and in the city you entered, a push notification will be sent to your device with show timings.

## To Do
1. Check for a movie in a city with price range.
2. Manage for task scheduling so it checks every x minutes till movie is found.
3. Handle exceptions during initial setup.

### License
 See the [LICENSE](LICENSE.md) file for license rights and limitations (GNU GPL v3)
