from dateutil.parser import parse


def convert_str2time(time: str):
    date = parse(time)
    return date.time()
