import requests
import os
from datetime import datetime, timedelta

# for get requests from open weather map
LAT = os.environ["MY_LAT"]
LON = os.environ["MY_LON"]
API_KEY = os.environ['API_KEY']
OPEN_WEATHER_API_END_POINT = "https://api.openweathermap.org/data/2.5/onecall"

rain_will_be_there = False

parameters = {
    "appid": API_KEY,
    "lat": LAT,
    "lon": LON,
    "exclude": "current,minutely,daily,alerts"
}
# GET API DATA
data = requests.get(OPEN_WEATHER_API_END_POINT, params=parameters).json()['hourly']

# this function will check weather conditions for 1 to next 48 hours
def check_rain(hour=12, all_weather_info=False):
    global rain_will_be_there
    hour_list = []
    weather_condition_on_that_day = {}
    rain_data_list = []
    value_check = 700
    if all_weather_info:
        value_check = 1000
    for i, hourly_weather in enumerate(data[:hour]):
        weather = hourly_weather['weather'][0]
        new_hour_ = datetime.now() + timedelta(hours=i+1)
        # required data will be get from open_weather_api
        if weather['id'] < value_check:
            rain_day = new_hour_.strftime('On %A (%d-%b-%Y)')
            if weather['id'] < 700:
                rain_will_be_there = True
            rain_time = f"{new_hour_.hour}"
            weather_condition = f"{weather['main']} ({weather['description']})"
            hour_list.append(rain_time)
            if weather_condition not in weather_condition_on_that_day.keys():
                weather_condition_on_that_day[weather_condition] = []
            weather_condition_on_that_day[weather_condition].append(rain_time)
            rain_data_list.append([rain_day] + [weather_condition] + [rain_time])

    # print(rain_data_list)
    # here we will arrange the data according to our need
    arranged_info = {}
    for rain in rain_data_list:
        if rain[0] not in arranged_info.keys():
            arranged_info[rain[0]] = [{rain[1]: [rain[2]]}]
        else:
            found = False
            for i in arranged_info[rain[0]]:
                if rain[1] in i.keys():
                    i[rain[1]].append(rain[2])
                    found = True
                    break
            if not found:
                new_key = {rain[1]: [rain[2]]}
                arranged_info[rain[0]].append(new_key)
    # print(arranged_info)
    return arranged_info
