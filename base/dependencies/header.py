from fastapi import Header

from base.exception.exception import NotFoundException


def check_account_header(account: str = Header(...)):
    if not account:
        raise NotFoundException('유저 정보가 존재하지 않습니다.')