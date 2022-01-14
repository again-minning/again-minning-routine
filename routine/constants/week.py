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
