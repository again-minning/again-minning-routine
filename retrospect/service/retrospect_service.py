from fastapi import UploadFile
from sqlalchemy.orm import Session

from base.exception.exception import MinningException
from base.utils.time import convert_str2datetime
from retrospect.constants.retrospect_message import RETROSPECT_NOT_FOUND_ID, RETROSPECT_NOT_FOUND_ROUTINE_DAYS, RETROSPECT_ALREADY_EXISTS
from retrospect.models.retrospect import Retrospect
from retrospect.repository.retrospect_repository import retrospect_exists_by, retrospect_join_image_find_by, find_retrospect_by_id_with, get_retrospect_list_by
from routine.constants.week import Week
from routine.repository.routine_repository import get_routine_day_with_routine_by


def create_retrospect(db: Session, routine_id: int, content: str, date: str, image: UploadFile, account: int):
    date = convert_str2datetime(date)
    weekday = Week.get_weekday(date.weekday())

    routine_with_days = get_routine_day_with_routine_by(db, routine_id, account, weekday)

    __check_retrospect(date, db, routine_with_days, routine_id)

    title = routine_with_days.routine.title
    retrospect: Retrospect = Retrospect(routine_id=routine_id, account_id=account, title=title, content=content, scheduled_date=date)
    if image:
        retrospect.add_image(url=image.filename)
    db.add(retrospect)
    db.commit()
    return True


def __check_retrospect(date, db, routine_days, routine_id):
    if not routine_days:
        raise MinningException(RETROSPECT_NOT_FOUND_ROUTINE_DAYS)
    is_exists_retrospects = retrospect_exists_by(db, routine_id, date)
    if is_exists_retrospects:
        raise MinningException(RETROSPECT_ALREADY_EXISTS)


def get_detail_retrospect(db: Session, retrospect_id: int, account: int):
    retrospect = retrospect_join_image_find_by(db, retrospect_id, account)

    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    return retrospect


def put_detail_retrospect(retrospect_id: int, content: str, image: UploadFile, db: Session, account: int):
    retrospect = retrospect_join_image_find_by(db, retrospect_id, account)
    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    retrospect.content = content
    if retrospect.image:
        retrospect.image.url = image.filename
    elif image:
        retrospect.add_image(url=image.filename)
    db.commit()
    return True


def delete_detail_retrospect(retrospect_id: int, db: Session, account: int):
    retrospect = find_retrospect_by_id_with(db, retrospect_id, account)
    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    db.delete(retrospect)
    db.commit()
    return True


def get_list_retrospect(date: str, db: Session, account_id: int):
    date = convert_str2datetime(date)
    result = get_retrospect_list_by(db, account_id, date)
    return result
