from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from base.utils.time import convert_str2time
from routine.models.routine import Routine
from routine.schemas import RoutineCreateRequest


def get_routine(db: Session, routine_id: int):
    return db.query(Routine).options(
        joinedload(Routine.days)).filter(
        and_(
            Routine.routine_id == routine_id,
            Routine.is_delete == False
        )
    ).all()


def create_routine(db: Session, routine: RoutineCreateRequest):
    days = routine.dict().pop('days')
    start_time = routine.start_time
    start_time = convert_str2time(start_time)
    db_routine = Routine(
        title=routine.title, category=routine.category,
        goal=routine.goal, start_time=start_time, account_id=routine.account_id
    )
    db_routine.add_days(days)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    return db_routine
