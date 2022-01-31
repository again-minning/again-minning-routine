from fastapi import Header
from base.constants.base_message import USER_NOT_FOUND
from base.exception.exception import MinningException


def check_account_header(account: str = Header(...)):
    if not account:
        raise MinningException(USER_NOT_FOUND)
