from weather_information import rain_will_be_there, check_rain
from create_message import get_message
from send_email_message import send_message, send_mail

# You can check 0, 48 hours rain data. It's your wish either 5, 12, 24,
# Add second True parameter if you want to check all weather conditions including clear sky
# if second parameter is False or left alone it will check for rain and snow etc
weather_data = check_rain(48, True)
message = get_message(weather_data)

if rain_will_be_there:
    # send SMS
    send_message(message)
    # send MAIL
    send_mail(message)
else:
    print("No rain")
#     # uncomment if you want to see message or send msg either rain or not
#     # print(message)
#     # send_message(message)
#     # send_mail(message)




