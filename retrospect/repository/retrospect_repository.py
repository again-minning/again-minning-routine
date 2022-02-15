from sqlalchemy import and_
from sqlalchemy.orm import contains_eager, Session, joinedload, load_only

from retrospect.models.retrospect import Retrospect
from routine.models.routine import Routine
from routine.models.routineDay import RoutineDay


def get_routine_days_join_routine_first(db: Session, account: int, routine_id: int, weekday):
    return db.query(
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


def exists_retrospect_by(db, routine_id, date):
    scheduled_retrospect = db.query(
        Retrospect
    ).filter(
        and_(
            Retrospect.scheduled_date == date,
            Retrospect.routine_id == routine_id
        )
    ).exists()
    return db.query(scheduled_retrospect).scalar()


def find_by_id_and_account(db, retrospect_id, account):
    return db.query(
        Retrospect
    ).filter(
        and_(
            Retrospect.id == retrospect_id,
            Retrospect.account_id == account
        )
    ).first()


def get_retrospect_with_image_by(db, retrospect_id, account):
    return db.query(
        Retrospect
    ).options(
        joinedload(Retrospect.image)
    ).filter(
        Retrospect.id == retrospect_id,
        Retrospect.account_id == account
    ).first()


def find_retrospect_list_by(db, account_id, date):
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
