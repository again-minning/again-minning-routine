from fastapi import UploadFile
from sqlalchemy.orm import Session

from base.database.database import commit
from base.exception.exception import MinningException
from base.utils.time import convert_str2datetime
from retrospect.constants.retrospect_message import RETROSPECT_NOT_FOUND_ID, RETROSPECT_NOT_FOUND_ROUTINE_DAYS, RETROSPECT_ALREADY_EXISTS
from retrospect.models.retrospect import Retrospect
from routine.constants.week import Week
from retrospect.repository.retrospect_repository import (get_routine_days_join_routine_first, get_retrospect_with_image_by,
                                                         find_by_id_and_account, exists_retrospect_by, find_retrospect_list_by)


@commit
def create_retrospect(db: Session, routine_id: int, content: str, date: str, image: UploadFile, account: int):
    date = convert_str2datetime(date)
    weekday = Week.get_weekday(date.weekday())
    routine_with_days = get_routine_days_join_routine_first(db, account, routine_id, weekday)
    __check_retrospect(date, db, routine_with_days, routine_id)
    title = routine_with_days.routine.title
    retrospect: Retrospect = Retrospect(routine_id=routine_id, account_id=account, title=title, content=content, scheduled_date=date)
    if image:
        retrospect.add_image(url=image.filename)
    db.add(retrospect)
    return True


def __check_retrospect(date, db, routine_days, routine_id):
    if not routine_days:
        raise MinningException(RETROSPECT_NOT_FOUND_ROUTINE_DAYS)
    is_exists_retrospects = exists_retrospect_by(db, routine_id, date)
    if is_exists_retrospects:
        raise MinningException(RETROSPECT_ALREADY_EXISTS)


def get_detail_retrospect(db: Session, retrospect_id: int, account: int):
    retrospect = get_retrospect_with_image_by(db, retrospect_id, account)
    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    return retrospect


@commit
def put_detail_retrospect(retrospect_id: int, content: str, image: UploadFile, db: Session, account: int):
    retrospect = get_retrospect_with_image_by(db, retrospect_id, account)
    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    retrospect.content = content
    if retrospect.image:
        retrospect.image.url = image.filename
    elif image:
        retrospect.add_image(url=image.filename)
    return True


@commit
def delete_detail_retrospect(retrospect_id: int, db: Session, account: int):
    retrospect = find_by_id_and_account(db, retrospect_id, account)
    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    db.delete(retrospect)
    return True


def get_list_retrospect(date: str, db: Session, account_id: int):
    date = convert_str2datetime(date)
    result = find_retrospect_list_by(db, account_id, date)
    return result
