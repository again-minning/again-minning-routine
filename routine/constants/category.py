from enum import Enum, unique


@unique
class Category(Enum):
    MIRACLE = 0
    SELF = 1
    HEALTH = 2
    DAILY = 3
    ETC = 4
