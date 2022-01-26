from sqlalchemy import and_
from sqlalchemy.orm import Session, load_only, subqueryload, joinedload

from base.utils.time import convert_str2time, convert_str2datetime
from routine.constants.result import Result
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult
from routine.schemas import RoutineCreateRequest, RoutineResultUpdateRequest


def get_routine_list(db: Session, account_id: str, today: str):
    fields = ['id', 'title', 'goal', 'start_time']

    today = convert_str2datetime(today)
    weekday = today.weekday()
    weekday = Week.get_weekday(weekday)

    routines = db.query(Routine).join(RoutineDay).filter(
        and_(
            Routine.account_id == account_id,
            Routine.is_delete == False,
            RoutineDay.day == weekday
        )
    ).options(load_only(*fields), joinedload(Routine.routine_results)).all()
    return routines, today


def create_routine(db: Session, routine: RoutineCreateRequest, account: str):
    days = routine.dict().pop('days')
    start_time = routine.start_time
    start_time = convert_str2time(start_time)

    db_routine = Routine(
        title=routine.title, category=routine.category,
        goal=routine.goal, start_time=start_time, account_id=account, is_alarm=routine.is_alarm
    )

    db_routine.init_days(days)
    db_routine.init_set_routine_result(days)
    db.add(db_routine)
    db.commit()
    return True


def update_or_create_routine_result(db: Session, routine_id: int, date: str, reqeust: RoutineResultUpdateRequest):
    result = reqeust.result
    yymmdd = convert_str2datetime(date)
    routine_result: RoutineResult = db.query(RoutineResult).filter(
        and_(RoutineResult.routine_id == routine_id,
             RoutineResult.yymmdd == yymmdd)
    ).first()
    if routine_result:
        routine_result.update_result(result)
    else:
        routine_result = RoutineResult(routine_id=routine_id, result=result, yymmdd=yymmdd)
        db.add(routine_result)
    db.commit()
    return True


def get_routine_detail(db: Session, routine_id: int):
    fields = ['title', 'category', 'start_time', 'goal', 'is_alarm']
    return db.query(Routine).filter(
        Routine.id == routine_id
    ).options(subqueryload('days').load_only('day'), load_only(*fields)).first()


def patch_routine_detail(db: Session, request: RoutineCreateRequest, routine_id: int, account: str):
    routine: Routine = db.query(Routine).filter(and_(Routine.id == routine_id, Routine.account_id == account)).first()
    routine.update_routine(request)
    request_days = set(request.days)
    routine.patch_days(db=db, request_days=request_days)
    db.commit()
    return True


def cancel_routine_results(db: Session, routine_id: int, date: str):
    date = convert_str2datetime(date)

    routine_result: RoutineResult = db.query(RoutineResult).filter(
        and_(
            RoutineResult.routine_id == routine_id,
            RoutineResult.yymmdd == date
        )
    ).first()

    routine_result.result = Result.NOT
    db.commit()
    return True
