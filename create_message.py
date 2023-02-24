class createFormattedMessage:
    def __init__(self, weather_information):
        self.weather_info = weather_information
        self.message = ""
        self.make_shape_of_weather_information()

    def make_shape_of_weather_information(self):
        for daily_date in self.weather_info:
            self.message += daily_date + "\n"
            for w_information in self.weather_info[daily_date]:
                for key, value in w_information.items():
                    self.message += key + ": at "
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
                                start = add_am_pm_to_hours(same_time_list[0])
                                end = add_am_pm_to_hours(same_time_list[-1], end_=True)
                                same_time_list = []
                                self.message += f"({start}-{end}), "
                                same_time_list.append(new_hour)
                                previous = new_hour
                                continue
                            # when match not found
                            else:
                                if len(same_time_list) == 1:
                                    same_time_list = []
                                    self.message += add_am_pm_to_hours(previous) + ", "
                                    same_time_list.append(new_hour)
                                else:
                                    same_time_list.append(new_hour)
                        previous = new_hour
                    # this last if else will check the last elements in same_time_list
                    if len(same_time_list) == 1 or not same_time_list:
                        self.message += add_am_pm_to_hours(previous) + ", "
                    else:
                        start = add_am_pm_to_hours(hour=same_time_list[0])
                        end = add_am_pm_to_hours(same_time_list[-1], end_=True)
                        self.message += f"({start}-{end}), "
                    self.message = self.message[:-2] + ".\n"
            self.message += "\n"
        self.message = self.message[:-2]

def add_am_pm_to_hours(hour, end_=False):
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
