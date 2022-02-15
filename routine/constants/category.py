from enum import Enum, unique


@unique
class Category(Enum):
    MIRACLE = 0
    SELF = 1
    HEALTH = 2
    DAILY = 3
    ETC = 4

    @classmethod
    def to_category(cls, index: int):
        if index == 0:
            return Category.MIRACLE
        elif index == 1:
            return Category.SELF
        elif index == 2:
            return Category.HEALTH
        elif index == 3:
            return Category.DAILY
        elif index == 4:
            return Category.ETC
        else:
            return None
