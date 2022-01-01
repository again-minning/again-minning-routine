from enum import Enum, unique


@unique
class HttpStatus(Enum):
    ROUTINE_OK = 'ROUTINE_OK'
    ROUTINE_CREATE_OK = 'ROUTINE_CREATE_OK'
