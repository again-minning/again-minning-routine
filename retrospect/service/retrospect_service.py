from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload, contains_eager, load_only

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
            RoutineDay.routine_id == routine_id,
            RoutineDay.day == weekday,
            Routine.account_id == account
        )
    ).first()

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
    scheduled_retrospect = db.query(
        Retrospect
    ).filter(
        and_(
            Retrospect.scheduled_date == date,
            Retrospect.routine_id == routine_id
        )
    ).exists()
    is_exists_retrospects = db.query(scheduled_retrospect).scalar()
    if is_exists_retrospects:
        raise MinningException(RETROSPECT_ALREADY_EXISTS)


def get_detail_retrospect(db: Session, retrospect_id: int, account: int):
    retrospect = db.query(
        Retrospect
    ).options(
        joinedload(Retrospect.image)
    ).filter(
        Retrospect.id == retrospect_id,
        Retrospect.account_id == account
    ).first()

    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    return retrospect


def put_detail_retrospect(retrospect_id: int, content: str, image: UploadFile, db: Session, account: int):
    retrospect = db.query(
        Retrospect
    ).options(
        joinedload(Retrospect.image)
    ).filter(
        Retrospect.id == retrospect_id,
        Retrospect.account_id == account
    ).first()
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
    retrospect = db.query(
        Retrospect
    ).filter(
        and_(
            Retrospect.id == retrospect_id,
            Retrospect.account_id == account
        )
    ).first()
    if not retrospect:
        raise MinningException(RETROSPECT_NOT_FOUND_ID)
    db.delete(retrospect)
    db.commit()
    return True


def get_list_retrospect(date: str, db: Session, account_id: int):
    date = convert_str2datetime(date)
    fields = ['id', 'routine_id', 'title', 'content']
    result = db.query(
        Retrospect
    ).options(
        joinedload(Retrospect.image)
    ).filter(
        and_(
            Retrospect.account_id == account_id,
            Retrospect.scheduled_date == date
        )
    ).options(
      load_only(*fields)
    ).order_by(
        Retrospect.created_at.desc()
    ).all()
    return result
