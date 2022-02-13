from sqlalchemy import and_
from sqlalchemy.orm import Session, load_only

from routine.models.routine import Routine
from routine.models.routineResult import RoutineResult


def get_routine_count(db: Session):
    return db.query(
        Routine
    ).filter(
        Routine.is_delete.is_(False)
    ).count()


def get_routine_pagination(db: Session, limit: int, offset: int):
    return db.query(
        Routine.id, Routine.title, Routine.category, Routine.account_id
    ).slice(limit, offset)


def get_routine_results_search_in(db: Session, routine_ids: list, start_date: str, end_date: str):
    fields = [RoutineResult.routine_id, RoutineResult.yymmdd, RoutineResult.result]
    return db.query(
        RoutineResult
    ).filter(
        and_(
            RoutineResult.routine_id.in_(routine_ids),
            RoutineResult.yymmdd.between(start_date, end_date)
        )
    ).options(
        load_only(*fields)
    ).all()
