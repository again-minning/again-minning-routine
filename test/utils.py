from base.utils.time import get_now, convert_str2date, convert_str2datetime


def get_now_date():
    now = str(get_now())
    day = str(convert_str2date(now))
    date = convert_str2datetime(day)
    return date
