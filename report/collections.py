from enum import Enum, unique


@unique
class Collections(str, Enum):
    REPORT = 'reports'
    MONTHLY_REPORT = 'monthly_reports'
