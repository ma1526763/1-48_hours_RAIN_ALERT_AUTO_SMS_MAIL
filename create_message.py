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
def get_message(weather_data):
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
