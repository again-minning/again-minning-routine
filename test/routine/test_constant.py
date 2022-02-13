from assertpy import assert_that

from routine.constants.category import Category
from routine.constants.week import week_get_index, Week


def test_category_static_method():
    assert_that(Category.to_category(0)).is_equal_to(Category.MIRACLE)
    assert_that(Category.to_category(1)).is_equal_to(Category.SELF)
    assert_that(Category.to_category(2)).is_equal_to(Category.HEALTH)
    assert_that(Category.to_category(3)).is_equal_to(Category.DAILY)
    assert_that(Category.to_category(4)).is_equal_to(Category.ETC)
    assert_that(Category.to_category(5)).is_none()


def test_week_get_index():
    assert_that(week_get_index(Week.MON)).is_zero()
    assert_that(week_get_index(Week.TUE)).is_equal_to(1)
    assert_that(week_get_index(Week.WED)).is_equal_to(2)
    assert_that(week_get_index(Week.THU)).is_equal_to(3)
    assert_that(week_get_index(Week.FRI)).is_equal_to(4)
    assert_that(week_get_index(Week.SAT)).is_equal_to(5)
    assert_that(week_get_index(Week.SUN)).is_equal_to(6)

    assert_that(week_get_index('MON')).is_zero()
    assert_that(week_get_index('TUE')).is_equal_to(1)
    assert_that(week_get_index('WED')).is_equal_to(2)
    assert_that(week_get_index('THU')).is_equal_to(3)
    assert_that(week_get_index('FRI')).is_equal_to(4)
    assert_that(week_get_index('SAT')).is_equal_to(5)
    assert_that(week_get_index('SUN')).is_equal_to(6)

    assert_that(week_get_index('PRI')).is_none()
