from datetime import date, datetime, timedelta


def datetime_to_string(time: date | datetime | timedelta | None):
    if type(time) == date or type(time) == datetime:
        datetime_object = datetime(year=time.year, month=time.month, day=time.day)
        return f"<t:{int(datetime_object.timestamp())}:D>"

    elif type(time) == timedelta:
        total_seconds = int(time.total_seconds())
        days, remainder = divmod(total_seconds, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 *60)
        minutes, seconds = divmod(remainder, 60)

        if days == 0:
            return f"{hours}h{minutes}m"
        elif days == 1:
            return f"{days} day, {hours}h{minutes}m"
        elif days > 1:
            return f"{days} days, {hours}h{minutes}m"

    return str(time)