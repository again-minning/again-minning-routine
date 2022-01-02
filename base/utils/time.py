from dateutil.parser import parse, ParserError


def convert_str2time(time: str):
    try:
        date = parse(time)
        return date.time()
    except ParserError:
        return None


def convert_str2date(date: str):
    try:
        date = parse(date)
        return date.date()
    except ParserError:
        return None
