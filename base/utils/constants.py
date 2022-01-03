from enum import Enum, unique


@unique
class HttpStatus(Enum):
    OK = 'OK'
    ROUTINE_OK = 'ROUTINE_OK'
    ROUTINE_CREATE_OK = 'ROUTINE_CREATE_OK'
