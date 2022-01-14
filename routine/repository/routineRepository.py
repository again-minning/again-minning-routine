from sqlalchemy import and_
from sqlalchemy import case, desc
from sqlalchemy.orm import Session, load_only

from base.utils.time import convert_str2time, convert_str2date
from routine.constants.result import Result
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult
from routine.schemas import RoutineCreateRequest


def check_routine(db: Session, routine_id: int):
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    routine.check_result(Result.DONE)
    db.add(routine)
    return True


def get_routine_list(db: Session, account_id: int, today: str):
    fields = ['id', 'title', 'goal', 'start_time']

    today = convert_str2date(today)
    weekday = today.weekday()
    weekday = Week.get_weekday(weekday)

    result = case([(RoutineResult.yymmdd == today, RoutineResult.result), ],
                  else_=Result.NOT).label('result')

    return db.query(Routine, result).join(RoutineResult).join(RoutineDay).filter(
        and_(
            Routine.account_id == account_id,
            Routine.is_delete == False,
            RoutineDay.day == weekday
        )
    ).options(load_only(*fields)).all()


def create_routine(db: Session, routine: RoutineCreateRequest):
    days = routine.dict().pop('days')
    start_time = routine.start_time
    start_time = convert_str2time(start_time)

    db_routine = Routine(
        title=routine.title, category=routine.category,
        goal=routine.goal, start_time=start_time, account_id=routine.account_id, is_alarm=routine.is_alarm
    )

    db_routine.add_days(days)
    db.add(db_routine)
    db.commit()
    return True


def delete_routine_for_test(db: Session):
    db.query(RoutineDay).delete()
    db.query(RoutineResult).delete()
    db.query(Routine).delete()
    return True


def get_routine_for_test(db: Session):
    routine = db.query(Routine).order_by(desc(Routine.id)).first()
    return routine


def get_routine_days_for_test(db: Session, routine_id: int):
    routine_days = db.query(RoutineDay).filter(RoutineDay.routine_id == routine_id).all()
    return routine_days


def get_routine_results_for_test(db: Session, routine_id: int):
    routine_results = db.query(RoutineResult).filter(RoutineResult.routine_id == routine_id).all()
    return routine_results
