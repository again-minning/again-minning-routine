from enum import Enum, unique


@unique
class HttpStatus(Enum):
    OK = 'OK'
    ROUTINE_OK = 'ROUTINE_OK'
    ROUTINE_LIST_OK = 'ROUTINE_LIST_OK'
    ROUTINE_DETAIL_OK = 'ROUTINE_DETAIL_OK'
    ROUTINE_CREATE_OK = 'ROUTINE_CREATE_OK'
    ROUTINE_PATCH_OK = 'ROUTINE_PATCH_OK'


@unique
class ConnectionMode(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    NONE = 'NONE'

