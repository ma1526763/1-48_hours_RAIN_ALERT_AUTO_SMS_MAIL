import requests
import os
from datetime import datetime, timedelta
from twilio.rest import Client
from smtplib import SMTP

# for get requests from open weather map
LAT = os.environ["MY_LAT"]
LON = os.environ["MY_LON"]
API_KEY = os.environ['API_KEY']
OPEN_WEATHER_API_END_POINT = "https://api.openweathermap.org/data/2.5/onecall"
# for sending SMS
TWILLIO_ACCOUNT_SID = os.environ["TWILLIO_SID"]
TWILLIO_AUTH_TOKEN = os.environ["TWILLIO_AUTH_TOKEN"]
TWILLIO_PHONE_NUMBER = os.environ["TWILLIO_PHONE_NUMBER"]
MY_PHONE_NUMBER = os.environ["MY_PHONE_NUMBER"]
# for sending mail
SENDER_MAIL = os.environ.get('SENDER_MAIL')
PASSWORD = os.environ.get('PASSWORD')
RECEIVER_MAIl = os.environ['RECEIVER_MAIL']

parameters = {
    "appid": API_KEY,
    "lat": LAT,
    "lon": LON,
    "exclude": "current,minutely,daily,alerts"
}
# GET API DATA
data = requests.get(OPEN_WEATHER_API_END_POINT, params=parameters).json()['hourly']
rain_will_be_there = False

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

# this function will make the decision either hour is Am, PM and more
def make_am_pm(hour, end_=False):
    if hour < 12:
        if hour == 0:
            hour = 12
        if end_:
            hour = f"{str(hour)}:59"
        hour = str(hour) + "AM"
    else:
        hour = hour % 12
        if hour == 0:
            hour = 12
        if end_:
            hour = f"{str(hour)}:59"

        hour = str(hour) + "PM"
    return hour

# This function will give you proper message on the base of days and make hours good
def get_message():
    message = ""
    for day_data in weather_data:
        message += day_data + "\n"
        for info in weather_data[day_data]:
            for key, value in info.items():
                message += key + ": at "
                previous = 40
                same_time_list = []
                # this loop will make the shape of hours
                for time in value:
                    new_hour = int(time)
                    if new_hour == previous + 1:
                        same_time_list.append(new_hour)
                        previous = new_hour
                        continue
                    else:
                        # when match found
                        if len(same_time_list) > 1:
                            start = make_am_pm(same_time_list[0])
                            end = make_am_pm(same_time_list[-1], end_=True)
                            same_time_list = []
                            message += f"({start}-{end}), "
                            same_time_list.append(new_hour)
                            previous = new_hour
                            continue
                        # when match not found
                        else:
                            if len(same_time_list) == 1:
                                same_time_list = []
                                message += make_am_pm(previous) + ", "
                                same_time_list.append(new_hour)
                            else:
                                same_time_list.append(new_hour)
                    previous = new_hour
                # this last if else will check the last elements in same_time_list
                if len(same_time_list) == 1 or not same_time_list:
                    message += make_am_pm(previous) + ", "
                else:
                    start = make_am_pm(hour=same_time_list[0])
                    end = make_am_pm(same_time_list[-1], end_=True)
                    message += f"({start}-{end}), "
                message = message[:-2] + ".\n"
        message += "\n"
    return message[:-2]

def send_message(message_to_send):
    client = Client(TWILLIO_ACCOUNT_SID, TWILLIO_AUTH_TOKEN)
    client.messages.create(body=message_to_send,
                           from_=TWILLIO_PHONE_NUMBER,
                           to=MY_PHONE_NUMBER
                           )
    print("message sent successfully")

def send_mail(message_to_send):
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=SENDER_MAIL, password=PASSWORD)
        connection.sendmail(from_addr=SENDER_MAIL, to_addrs=RECEIVER_MAIl, msg=f"Subject:WEATHER INFORMATION\n\n{message_to_send}")
        print("mail sent successfully")

# You can check 0, 48 hours rain data. It's your wish either 5, 12, 24,
# Add second True parameter if you want to check all weather conditions including clear sky
# if second parameter is False or left alone it will check for rain and snow etc
weather_data = check_rain(48, True)

if rain_will_be_there:
    message_to = get_message()
    # send SMS
    send_message(message_to)
    # send MAIL
    send_mail(message_to)


# uncomment if you want to see message or send msg either rain or not
# message_ = get_message()
# print(message)
# send SMS
# send_message(message_)
# send MAIL
# print(message_)
# send_mail(message_)
