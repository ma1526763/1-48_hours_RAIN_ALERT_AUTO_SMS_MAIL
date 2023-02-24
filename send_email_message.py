import os
from twilio.rest import Client
from smtplib import SMTP


# for sending SMS
TWILLIO_ACCOUNT_SID = os.environ["TWILLIO_SID"]
TWILLIO_AUTH_TOKEN = os.environ["TWILLIO_AUTH_TOKEN"]
TWILLIO_PHONE_NUMBER = os.environ["TWILLIO_PHONE_NUMBER"]
MY_PHONE_NUMBER = os.environ["MY_PHONE_NUMBER"]
# for sendi ng mail
SENDER_MAIL = os.environ.get('SENDER_MAIL')
PASSWORD = os.environ.get('PASSWORD')
RECEIVER_MAIl = os.environ['RECEIVER_MAIL']


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