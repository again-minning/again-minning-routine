from sqlalchemy import and_
from sqlalchemy import case
from sqlalchemy.orm import Session, load_only

from base.utils.time import convert_str2time, convert_str2date, convert_str2datetime
from routine.constants.result import Result
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult
from routine.schemas import RoutineCreateRequest, RoutineResultUpdateRequest


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
    return True


def update_or_create_routine_result(db: Session, routine_id: int, reqeust: RoutineResultUpdateRequest):
    result = reqeust.result
    weekday = reqeust.weekday
    yymmdd = convert_str2datetime(reqeust.date)
    routine_result = db.query(RoutineResult).filter(
        and_(RoutineResult.routine_id == routine_id,
             RoutineResult.yymmdd == yymmdd)
    ).first()
    if routine_result:
        routine_result.result = result
        db.add(routine_result)
    else:
        routine_result = RoutineResult(routine_id=routine_id, result=result, yymmdd=yymmdd, week_day=weekday.value)
        db.add(routine_result)
    return True
