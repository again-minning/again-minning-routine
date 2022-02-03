from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload, contains_eager

from base.exception.exception import MinningException
from base.utils.time import convert_str2datetime
from retrospect.constants.retrospect_message import RETROSPECT_NOT_FOUND_ID, RETROSPECT_NOT_FOUND_ROUTINE_DAYS, RETROSPECT_ALREADY_EXISTS
from retrospect.models.retrospect import Retrospect
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay


def create_retrospect(db: Session, routine_id: int, content: str, date: str, image: UploadFile, account: int):
    date = convert_str2datetime(date)
    weekday = Week.get_weekday(date.weekday())

    routine_with_days = db.query(
        RoutineDay
    ).join(
        RoutineDay.routine
    ).options(
        contains_eager(RoutineDay.routine)
    ).filter(
        and_(
            RoutineDay.routine_id.is_(routine_id),
            RoutineDay.day.is_(weekday),
            Routine.account_id.is_(account)
        )
    ).first()

    __check_retrospect(date, db, routine_with_days, routine_id)

    title = routine_with_days.routine.title
    retrospect: Retrospect = Retrospect(routine_id=routine_id, title=title, content=content, scheduled_date=date)
    if image:
        retrospect.add_image(url=image.filename)
    db.add(retrospect)
    db.commit()
    return True


def get_detail_retrospect(db: Session, retrospect_id: int):
    retrospect = db.query(
        Retrospect
    ).options(
        joinedload(Retrospect.image)
    ).filter(
        Retrospect.id.is_(retrospect_id)
    ).first()

    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    return retrospect


def put_detail_retrospect(retrospect_id: int, content: str, image: UploadFile, db: Session):
    retrospect = db.query(
        Retrospect
    ).options(
        joinedload(Retrospect.image)
    ).filter(
        Retrospect.id.is_(retrospect_id)
    ).first()

    retrospect.content = content
    if retrospect.image:
        retrospect.image.url = image.filename
    elif image:
        retrospect.add_image(url=image.filename)
    retrospect.update_modified_at()
    db.commit()
    return True


def delete_detail_retrospect(retrospect_id: int, db: Session):
    db.query(Retrospect).filter(Retrospect.id.is_(retrospect_id)).delete()
    return True
