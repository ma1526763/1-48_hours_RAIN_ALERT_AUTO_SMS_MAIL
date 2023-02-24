import os
from weather_information import weatherInformation
from create_message import createFormattedMessage
from send_email_message import send_message, send_mail
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# longitude range b/w [-180, 180], latitude range b/w [-90, 90]
all_weather_info = True

def validate_all_entry_data(latitude, longitude, hours):
    # default values for longitude, latitude, hours
    latitude = os.environ["MY_LAT"] if not latitude else latitude
    longitude = os.environ["MY_LON"] if not longitude else longitude
    hours = 48 if not hours else hours
    # validate lat, long, hours, with datatype
    try:
        latitude, longitude = float(latitude), float(longitude)
        if latitude < -90 or latitude > 90:
            return messagebox.showerror(title="INVALID LATITUDE", message="PLEASE ENTER LATITUDE b/w [-90,90].")
        if longitude < -180 or longitude > 180:
            return messagebox.showerror(title="INVALID LONGITUDE", message="PLEASE ENTER LONGITUDE b/w [-180,180].")
    except ValueError:
        return messagebox.showerror(title="INVALID LAT/LONG", message="PLEASE ENTER VALID LATITUDE/LONGITUDE.")
    try:
        hours = int(hours)
        if hours <= 0 or hours > 48:
            return messagebox.showerror(title="INVALID HOURS TYPE", message="PLEASE ENTER HOURS 1-48")
    except ValueError:
        return messagebox.showerror(title="INVALID HOURS TYPE", message="PLEASE ENTER HOURS 1-48")
    return latitude, longitude, hours

def check_rain_only():
    global all_weather_info
    all_weather_info = False
    check_weather()

def check_weather():
    global all_weather_info
    try:
        lat, long, hours = validate_all_entry_data(latitude_entry.get(), longitude_entry.get(), hours_entry.get())
    except ValueError:
        return clear_entry()
    weather = weatherInformation(lat=lat, long=long, hours=hours, all_weather_info=all_weather_info)
    all_weather_info = True
    format_message = createFormattedMessage(weather.weather_information)
    if not format_message.message:
        messagebox.showinfo(title="NO RAIN", message=f"There will be no rain in your area for next {hours} hours.")
        return clear_entry()
    file_name = "RAIN_" if weather.rain else "NO_RAIN_"
    file_name += f"{datetime.now().strftime('%b-%d-%Y')}__LAT_{round(lat, 3)}__LONG_{round(long, 3)}__for__{hours}_hours.txt"
    with open(file_name, "w") as file:
        file.write(format_message.message)

    # messagebox.showinfo(title="SUCCESSFULL", message="PLEASE CHECK FILE FOR THE DATA.")
    send_mail(format_message.message)
    send_message(format_message.message)
    clear_entry()
def clear_entry():
    latitude_entry.delete(0, END)
    longitude_entry.delete(0, END)
    hours_entry.delete(0, END)
    latitude_entry.focus()

################# GUI #################
window = Tk()
window.title("Cheap Flight")
window.geometry("1200x674+0+0")
window.resizable(False, False)
canvas = Canvas(width=1200, height=674)
canvas.place(x=0, y=0)

img = PhotoImage(file="img.png")
canvas.create_image(600, 337, image=img)
COLOR_1 = "#051824"
COLOR_2 = "#134872"
COLOR_3 = "#316fac"
COLOR_4 = "#5777b3"

latitude_label = Label(text="Latitude", background=COLOR_2, foreground="white", font=("Arial", 22, "bold"))
latitude_label.place(x=315, y=120)
latitude_entry = Entry(width=15, font=("Arial", 22), highlightthickness=2, highlightbackground=COLOR_1,
                       highlightcolor=COLOR_1)
latitude_entry.grid(row=0, column=1, padx=200, pady=20)
latitude_entry.place(x=462, y=120)
latitude_entry.focus()
# Longitude
longitude_label = Label(text="Longitude", background=COLOR_2, foreground="white", font=("Arial", 22, "bold"))
longitude_label.place(x=300, y=170)
longitude_entry = Entry(width=15, font=("Arial", 22), highlightthickness=2, highlightbackground=COLOR_1,
                        highlightcolor=COLOR_1)
longitude_entry.place(x=462, y=170)
# Hours
hours_label = Label(text="Hours", background=COLOR_2, foreground="white", font=("Arial", 22, "bold"))
hours_label.place(x=330, y=220)
hours_entry = Entry(width=15, font=("Arial", 22), highlightthickness=2, highlightbackground=COLOR_1,
                    highlightcolor=COLOR_1)
hours_entry.place(x=462, y=220)
# BUTTONS
cheap_flights_button = Button(text="COMPLETE WEATHER", background=COLOR_2, foreground="white",
                              font=("Arial", 15, "bold"), command=check_weather)
cheap_flights_button.place(x=462, y=285, width=250)
cheap_flights_in_6_month_button = Button(text="ONLY RAIN", background=COLOR_4, foreground="white",
                                         font=("Arial", 15, "bold",), command=check_rain_only)
cheap_flights_in_6_month_button.place(x=462, y=335, width=250)

window.mainloop()
