# Movie Alert
A script written in Python to send a PushBullet notification when a particular movie hits the movie hall of your choice listed on Bookmyshow.

### Requirements

  1. Install [Python 3.4](https://www.python.org/download/releases/3.4.3/)  
  2. Install requests, beautifulsoup4, websocket-client using pip.

      * requests - `pip install requests`
      * beautifulsoup4 - `pip install beautifulsoup4`
      * websocket-client - `pip install websocket-client`  

  3. Collect your PushBullet access token from [here](https://www.pushbullet.com/account)  

### Usage

Before you run `movie_alert.py`, you need to collect a few details and enter them in `movie_alert.py`.  

  1. Enter the movie name in `movie_name`
  2. Enter language in `language`  
  3. Enter month and date in `month` and `day`
  4. Enter the movie hall URL in `bookmyshow_URL`
  5. Enter access token in `access_token`
  6. Modify `device_index` based on listing from [PushBullet.com](https://www.pushbullet.com/edit-devices)  
  `0` for first device, `1` for second and so on.

Now run `python movie_alert.py` from project directory in command prompt. If a movie is playing in the hall on the particular date, a push notification will be sent to your device with show timings.

### To Do

  1. Check for a movie in a city.
  2. Manage for task scheduling so it checks every x minutes till movie is found.
  3. Handle exceptions.
