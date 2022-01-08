from assertpy import assert_that

from base.utils.time import DateUtil
from datetime import datetime


def test_윤년이_아니고_2월_달_이전달_시작과_끝():
    # given
    day = datetime.fromisoformat('2022-02-07')
    # when
    start, end = DateUtil().return_prev_between_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2022-01-01'))
    assert_that(end).is_equal_to(datetime.fromisoformat('2022-01-31'))


def test_윤년이_아니고_2월_달_이전달_시작():
    # given
    day = datetime.fromisoformat('2022-02-07')
    # when
    start_date = DateUtil().return_prev_start_date(day)
    # then
    assert_that(start_date).is_equal_to(datetime.fromisoformat('2022-01-01'))


def test_윤년이_아니고_2월_달_이전달_끝():
    # given
    day = datetime.fromisoformat('2022-02-07')
    # when
    end_date = DateUtil().return_prev_end_date(day)
    # then
    assert_that(end_date).is_equal_to(datetime.fromisoformat('2022-01-31'))


def test_윤년이_아니고_30일인_날_이전달_시작과_끝():
    # given
    day = datetime.fromisoformat('2022-04-07')
    # when
    start, end = DateUtil().return_prev_between_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2022-03-01'))
    assert_that(end).is_equal_to(datetime.fromisoformat('2022-03-31'))


def test_윤년이_아니고_30일인_날_이전달_시작():
    # given
    day = datetime.fromisoformat('2022-09-30')
    # when
    start = DateUtil().return_prev_start_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2022-08-01'))


def test_윤년이_아니고_30일인_날_이전달_끝():
    # given
    day = datetime.fromisoformat('2022-11-01')
    # when
    end = DateUtil().return_prev_end_date(day)
    # then
    assert_that(end).is_equal_to(datetime.fromisoformat('2022-10-31'))


def test_윤년이_아니고_31일인_날_이전달_시작과_끝():
    # given
    day = datetime.fromisoformat('2022-01-01')
    # when
    start, end = DateUtil().return_prev_between_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2021-12-01'))
    assert_that(end).is_equal_to(datetime.fromisoformat('2021-12-31'))


def test_윤년이_아니고_31일인_날_이전달_시작():
    # given
    day = datetime.fromisoformat('2022-01-31')
    # when
    start = DateUtil().return_prev_start_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2021-12-01'))


def test_윤년이_아니고_31일인_날_이전달_끝():
    # given
    day = datetime.fromisoformat('2022-12-31')
    # when
    end = DateUtil().return_prev_end_date(day)
    # then
    assert_that(end).is_equal_to(datetime.fromisoformat('2022-11-30'))


def test_윤년이고_2월_달_이전달_시작과_끝():
    # given
    day = datetime.fromisoformat('2000-02-29')
    # when
    start, end = DateUtil().return_prev_between_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2000-01-01'))
    assert_that(end).is_equal_to(datetime.fromisoformat('2000-01-31'))


def test_윤년이고_2월_달_이전달_시작():
    # given
    day = datetime.fromisoformat('2000-02-28')
    # when
    start = DateUtil().return_prev_start_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2000-01-01'))


def test_윤년이고_2월_달_이전달_끝():
    # given
    day = datetime.fromisoformat('2000-02-01')
    # when
    end = DateUtil().return_prev_end_date(day)
    # then
    assert_that(end).is_equal_to(datetime.fromisoformat('2000-01-31'))


def test_윤년이고_30일인_날_이전달_시작과_끝():
    # given
    day = datetime.fromisoformat('2000-04-30')
    # when
    start, end = DateUtil().return_prev_between_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2000-03-01'))
    assert_that(end).is_equal_to(datetime.fromisoformat('2000-03-31'))


def test_윤년이고_30일인_날_이전달_시작():
    # given
    day = datetime.fromisoformat('2000-04-01')
    # when
    start= DateUtil().return_prev_start_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('2000-03-01'))


def test_윤년이고_30일인_날_이전달_끝():
    # given
    day = datetime.fromisoformat('2000-11-30')
    # when
    end = DateUtil().return_prev_end_date(day)
    # then
    assert_that(end).is_equal_to(datetime.fromisoformat('2000-10-31'))


def test_윤년이고_31일인_날_이전달_시작과_끝():
    # given
    day = datetime.fromisoformat('2000-01-01')
    # when
    start, end = DateUtil().return_prev_between_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('1999-12-01'))
    assert_that(end).is_equal_to(datetime.fromisoformat('1999-12-31'))


def test_윤년이고_31일인_날_이전달_시작():
    # given
    day = datetime.fromisoformat('2000-01-31')
    # when
    start = DateUtil().return_prev_start_date(day)
    # then
    assert_that(start).is_equal_to(datetime.fromisoformat('1999-12-01'))


def test_윤년이고_31일인_날_이전달_끝():
    # given
    day = datetime.fromisoformat('2000-12-31')
    # when
    end = DateUtil().return_prev_end_date(day)
    # then
    assert_that(end).is_equal_to(datetime.fromisoformat('2000-11-30'))
