
from dateutil.parser import parse, ParserError
from datetime import timedelta
from pytz import timezone, utc
import datetime

KST = timezone('Asia/Seoul')


def get_now() -> datetime.datetime:
    now = datetime.datetime.utcnow()
    return utc.localize(now).astimezone(KST)


def default_date():
    return datetime.datetime.fromisoformat('1900-01-01')


def get_today_end():
    tomorrow = get_now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return tomorrow - timedelta(microseconds=1)


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


class DateUtil:
    __MONTH = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    def check_leap_year(self, year):
        if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
            self.__MONTH[2] = 29
        else:
            self.__MONTH[2] = 28

    def end_of_month(self, year, month):
        self.check_leap_year(year)
        if type(month) is str and month.isdigit():
            pass
        elif type(month) is int:
            pass
        else:
            raise ValueError('숫자로 된 값을 넣어주세요')

        if month == 0:
            month = 12

        if month == 13:
            month = 1

        if not (1 <= int(month) <= 12):
            raise ValueError(' 1 이상 12 이하의 값을 넣어주세요')

        return self.__MONTH[month]

    def prev_end_of_month(self, year, month):
        return self.end_of_month(year, month - 1)

    def return_prev_start_date(self, date):
        delta = date.day
        return (date - timedelta(days=delta)).replace(day=1)

    def return_prev_end_date(self, date):
        delta = date.day
        return (
                date - timedelta(days=delta)
        ).replace(day=self.prev_end_of_month(year=date.year, month=date.month))

    def return_prev_between_date(self, date):
        return self.return_prev_start_date(date), self.return_prev_end_date(date)
