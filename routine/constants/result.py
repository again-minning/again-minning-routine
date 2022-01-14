from enum import Enum, unique


@unique
class Result(str, Enum):
    NOT = 'NOT'
    TRY = 'TRY'
    DONE = 'DONE'
    DEFAULT = 'DEFAULT'
