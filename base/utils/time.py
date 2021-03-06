
import datetime
import re
from datetime import timedelta

from dateutil.parser import parse, ParserError
from pytz import timezone, utc

from base.exception.exception import MinningException
from routine.constants.routine_message import ROUTINE_FIELD_DATE_ERROR_MESSAGE, ROUTINE_UPDATE_PERIOD_OVER_RESPONSE
from routine.constants.week import Week, week_get_index

KST = timezone('Asia/Seoul')


def get_now() -> datetime.datetime:
    now = datetime.datetime.utcnow()
    return utc.localize(now).astimezone(KST)


def get_last_week_about(date: datetime.datetime, week: Week):
    return date - timedelta(days=date.weekday()) - timedelta(days=7) + timedelta(days=week_get_index(week))


def get_end_datetime(date: datetime.datetime):
    return date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) - timedelta(microseconds=1)


def get_start_datetime(date: datetime.datetime):
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


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


def convert_str2datetime(date: str):
    try:
        date = parse(date)
        date.astimezone(KST)
        return date
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
            raise ValueError('????????? ??? ?????? ???????????????')

        if month == 0:
            month = 12

        if month == 13:
            month = 1

        if not (1 <= int(month) <= 12):
            raise ValueError(' 1 ?????? 12 ????????? ?????? ???????????????')

        return self.__MONTH[month]

    def prev_end_of_month(self, year, month):
        return self.end_of_month(year, month - 1)

    def return_prev_start_date(self, date):
        delta = date.day
        return (date - timedelta(days=delta)).replace(day=1)

    def return_prev_end_date(self, date):
        delta = date.day
        return (date - timedelta(days=delta)).replace(day=self.prev_end_of_month(year=date.year, month=date.month))

    def return_prev_between_date(self, date):
        return self.return_prev_start_date(date), self.return_prev_end_date(date)


def validate_date(request):
    regex = re.compile(r'^[\d]{4}-[\d]{2}-[\d]{2}$')
    valid = regex.search(request)
    if valid is None:
        raise ValueError(ROUTINE_FIELD_DATE_ERROR_MESSAGE)
    return request


def check_is_modified_period(request: str):
    date = convert_str2datetime(request)
    now = get_now()
    diff_days = now.day - date.day
    if diff_days >= 3:
        raise MinningException(ROUTINE_UPDATE_PERIOD_OVER_RESPONSE)
