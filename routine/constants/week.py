from enum import Enum, unique


@unique
class Week(str, Enum):
    MON = 'MON'
    TUE = 'TUE'
    WED = 'WED'
    THU = 'THU'
    FRI = 'FRI'
    SAT = 'SAT'
    SUN = 'SUN'

    @classmethod
    def get_weekday(cls, index: int):
        if index == 0:
            return Week.MON
        elif index == 1:
            return Week.TUE
        elif index == 2:
            return Week.WED
        elif index == 3:
            return Week.THU
        elif index == 4:
            return Week.FRI
        elif index == 5:
            return Week.SAT
        elif index == 6:
            return Week.SUN
        else:
            return None


def week_get_index(week: Week):
    if week == Week.MON:
        return 0
    elif week == Week.TUE:
        return 1
    elif week == Week.WED:
        return 2
    elif week == Week.THU:
        return 3
    elif week == Week.FRI:
        return 4
    elif week == Week.SAT:
        return 5
    elif week == Week.SUN:
        return 6
    else:
        return None
