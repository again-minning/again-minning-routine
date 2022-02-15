from sqlalchemy import and_
from sqlalchemy.orm import Session, load_only, joinedload, subqueryload, contains_eager

from routine.constants.week import Week
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult


def find_by_account_and_weekday(db: Session, account_id: int, weekday: Week):
    fields = ['id', 'title', 'goal', 'start_time']
    return db.query(
        Routine
    ).join(
        RoutineDay
    ).filter(
        and_(
            Routine.account_id == account_id,
            Routine.is_delete.is_(False),
            RoutineDay.day == weekday
        )
    ).options(
        load_only(*fields),
        joinedload(Routine.routine_results)
    ).all()


def save_routine(db, routine, account, days, start_time):
    db_routine = Routine(
        title=routine.title, category=routine.category,
        goal=routine.goal, start_time=start_time, account_id=account, is_alarm=routine.is_alarm
    )
    db_routine.init_days(days)
    db_routine.init_set_routine_result(days)
    db.add(db_routine)
    db.commit()


def get_routine_result(db, routine_id, yymmdd):
    return db.query(
        RoutineResult
    ).filter(
        and_(
            RoutineResult.routine_id == routine_id,
            RoutineResult.yymmdd == yymmdd
        )
    ).first()


def find_detail_routine(db, routine_id, account):
    fields = ['title', 'category', 'start_time', 'goal', 'is_alarm']
    return db.query(
        Routine
    ).filter(
        and_(
            Routine.id == routine_id,
            Routine.account_id == account
        )
    ).options(
        subqueryload('days').load_only('day'),
        load_only(*fields)
    ).first()


def find_by_id_about_account(db, routine_id, account):
    return db.query(
        Routine
    ).filter(
        and_(
            Routine.id == routine_id,
            Routine.account_id == account
        )
    ).first()


def find_results_join_routine(db, routine_id, date):
    return db.query(
        RoutineResult
    ).join(
        RoutineResult.routine
    ).options(
        contains_eager(RoutineResult.routine)
    ).filter(
        and_(
            RoutineResult.routine_id == routine_id,
            RoutineResult.yymmdd == date
        )
    ).first()


def delete_by_id_about_account(db, routine_id, account):
    db.query(
        Routine
    ).filter(
        and_(
            Routine.id == routine_id,
            Routine.account_id == account
        )
    ).delete()


def get_routine_days(db, account_id, day):
    return db.query(RoutineDay).join(Routine).filter(
        and_(
            RoutineDay.day == day,
            Routine.account_id == account_id
        )
    ).all()
