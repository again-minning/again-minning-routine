from fastapi import UploadFile
from sqlalchemy import and_
from sqlalchemy.orm import Session

from base.exception.exception import NotFoundException
from base.utils.time import convert_str2datetime
from retrospect.constants.retrospect_message import *
from retrospect.models.retrospect import Retrospect
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay


def create_retrospect(db: Session, routine_id: int, title: str, content: str, date: str, image: UploadFile, account: int):
    date = convert_str2datetime(date)
    weekday = Week.get_weekday(date.weekday())
    routine_days = db.query(RoutineDay).join(Routine).filter(and_(Routine.id == routine_id, RoutineDay.day == weekday, Routine.account_id == account)).exists()
    is_exists = db.query(routine_days).scalar()
    if not is_exists:
        raise NotFoundException(RETROSPECT_NOT_FOUND_ROUTINE_DAYS)
    retrospect: Retrospect = Retrospect(routine_id=routine_id, title=title, content=content, scheduled_date=date)
    if image:
        retrospect.add_image(url=image.filename)
    db.add(retrospect)
    db.commit()
    return True
