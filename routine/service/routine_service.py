from sqlalchemy.orm import Session

from base.constants.base_message import USER_INFO_NOT_EQUAL
from base.database.database import commit
from base.exception.exception import MinningException
from base.utils.time import convert_str2time, convert_str2datetime
from routine.constants.result import Result
from routine.constants.routine_message import ROUTINE_NO_DATA_RESPONSE
from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineResult import RoutineResult
from routine.repository.routine_repository import (find_by_account_and_weekday, save_routine,
                                                   get_routine_result, find_detail_routine,
                                                   find_by_id_about_account, find_results_join_routine,
                                                   delete_by_id_about_account, get_routine_days)
from routine.schemas import RoutineCreateRequest, RoutineResultUpdateRequest, RoutineSequenceRequest


def get_routine_list(db: Session, account_id: int, today: str):
    today = convert_str2datetime(today)
    weekday = today.weekday()
    weekday = Week.get_weekday(weekday)
    routines = find_by_account_and_weekday(db=db, account_id=account_id, weekday=weekday)
    return routines, today


def create_routine(db: Session, routine: RoutineCreateRequest, account: int):
    days = routine.dict().pop('days')
    start_time = routine.start_time
    start_time = convert_str2time(start_time)
    save_routine(db, routine, account, days, start_time)
    return True


@commit
def update_or_create_routine_result(db: Session, routine_id: int, date: str, reqeust: RoutineResultUpdateRequest):
    result = reqeust.result
    yymmdd = convert_str2datetime(date)
    routine_result: RoutineResult = get_routine_result(db, routine_id, yymmdd)
    if routine_result:
        routine_result.update_result(result)
    else:
        routine_result = RoutineResult(routine_id=routine_id, result=result, yymmdd=yymmdd)
        db.add(routine_result)
    return True


def get_routine_detail(db: Session, routine_id: int, account: int):
    return find_detail_routine(db, routine_id, account)


@commit
def patch_routine_detail(db: Session, request: RoutineCreateRequest, routine_id: int, account: int):
    routine: Routine = find_by_id_about_account(db, routine_id, account)
    if routine is None:
        raise MinningException(name=ROUTINE_NO_DATA_RESPONSE)
    routine.update_routine(request)
    request_days = set(request.days)
    routine.patch_days(db=db, request_days=request_days)
    return True


@commit
def cancel_routine_results(db: Session, routine_id: int, date: str, account: int):
    date = convert_str2datetime(date)

    routine_result: RoutineResult = find_results_join_routine(db, routine_id, date)
    if routine_result is None:
        raise MinningException(name=ROUTINE_NO_DATA_RESPONSE)
    if routine_result.routine.account_id != account:
        raise MinningException(name=USER_INFO_NOT_EQUAL)
    routine_result.result = Result.NOT
    return True


@commit
def delete_routine(db: Session, routine_id: int, account: int):
    routine = find_by_id_about_account(db=db, routine_id=routine_id, account=account)
    if routine is None:
        raise MinningException(name=ROUTINE_NO_DATA_RESPONSE)
    delete_by_id_about_account(db, routine_id, account)
    return True


@commit
def change_routine_sequence(db: Session, weekday: int, account_id: int, routine_sequences: RoutineSequenceRequest):
    day = Week.get_weekday(weekday)
    routine_days = get_routine_days(db, account_id, day)

    routine_sequence_dicts = routine_sequences.to_dict()
    for routine_day in routine_days:
        routine_day.sequence = routine_sequence_dicts[routine_day.routine_id]
    return True
