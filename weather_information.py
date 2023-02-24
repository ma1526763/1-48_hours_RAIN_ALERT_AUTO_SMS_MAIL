import requests
import os
from datetime import datetime, timedelta

class weatherInformation:
    def __init__(self, lat, long, hours, all_weather_info=False):
        self.lat = lat
        self.long = long
        self.hours = hours
        self.all_weather_info = all_weather_info
        self.rain = False
        self.timezone = None
        self.api_key = os.environ['API_KEY']
        self.open_weather_endpoint = 'https://api.openweathermap.org/data/2.5/onecall'
        self.hourly_weather_data = None
        self.hours_list = []
        self.rain_or_all_weather_info = []
        self.weather_condition_on_specific_day = {}
        self.weather_information = {}
        self.get_weather_data_in_json_format()
        self.check_rain_or_all_weather_info()
        self.arrange_weather_information()

    def get_weather_data_in_json_format(self):
        weather_params = {
            "appid": self.api_key,
            "lat": self.lat,
            "lon": self.long,
            "exclude": "current,daily,alerts"
        }
        data = requests.get(self.open_weather_endpoint, params=weather_params).json()

        self.timezone = data['timezone']
        self.hourly_weather_data = data['hourly']

    def check_rain_or_all_weather_info(self):
        weather_check_value = 1000 if self.all_weather_info else 700
        for i, hourly_weather in enumerate(self.hourly_weather_data[:self.hours]):
            hourly_weather = hourly_weather['weather'][0]
            new_hour = datetime.now() + timedelta(hours=i + 1)
            if hourly_weather['id'] < weather_check_value:
                weather_day = new_hour.strftime('On %A (%d-%b-%Y)')
                if hourly_weather['id'] < 700:
                    self.rain = True
                new_hour = f"{new_hour.hour}"
                weather_condition = f"{hourly_weather['main']} ({hourly_weather['description']})"
                self.hours_list.append(new_hour)
                # new weather condition
                if weather_condition not in self.weather_condition_on_specific_day.keys():
                    self.weather_condition_on_specific_day[weather_condition] = []
                # appending new hour with weather condition
                self.weather_condition_on_specific_day[weather_condition].append(new_hour)
                self.rain_or_all_weather_info.append([weather_day] + [weather_condition] + [new_hour])

    def arrange_weather_information(self):
        for weather_info_in_that_hour in self.rain_or_all_weather_info:
            if weather_info_in_that_hour[0] not in self.weather_information.keys():
                self.weather_information[weather_info_in_that_hour[0]] = [{weather_info_in_that_hour[1]: [weather_info_in_that_hour[2]]}]
            else:
                found = False
                for i in self.weather_information[weather_info_in_that_hour[0]]:
                    if weather_info_in_that_hour[1] in i.keys():
                        i[weather_info_in_that_hour[1]].append(weather_info_in_that_hour[2])
                        found = True
                        break
                if not found:
                    new_key = {weather_info_in_that_hour[1]: [weather_info_in_that_hour[2]]}
                    self.weather_information[weather_info_in_that_hour[0]].append(new_key)
