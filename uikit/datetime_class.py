from datetime import datetime, timedelta, date


class Time:
    def __init__(self, time_object: datetime | timedelta):
        self.time = time_object

    def __str__(self):
        if type(self.time) != timedelta:
            datetime_string = datetime.strftime(self.time, "%B %d, %Y")
            return datetime_string
        elif type(self.time) == timedelta:
            total_seconds = int(self.time.total_seconds())
            days, remainder = divmod(total_seconds, 24 * 60 * 60)
            hours, remainder = divmod(remainder, 60*60)
            minutes, seconds = divmod(remainder, 60)

            if days == 0:
                return f"{hours}h{minutes}m"
            elif days == 1:
                return f"{days} day, {hours}h{minutes}m"
            elif days > 1:
                return f"{days} days, {hours}h{minutes}m"
        return str(self.time)
