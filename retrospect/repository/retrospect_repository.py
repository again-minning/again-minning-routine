from sqlalchemy import and_
from sqlalchemy.orm import joinedload, load_only

from retrospect.models.retrospect import Retrospect


def retrospect_exists_by(db, routine_id, date):
    scheduled_retrospect = db.query(
        Retrospect
    ).filter(
        and_(
            Retrospect.scheduled_date == date,
            Retrospect.routine_id == routine_id
        )
    ).exists()
    is_exists_retrospects = db.query(scheduled_retrospect).scalar()
    return is_exists_retrospects


def find_retrospect_by_id_with(db, retrospect_id, account):
    return db.query(
        Retrospect
    ).filter(
        and_(
            Retrospect.id == retrospect_id,
            Retrospect.account_id == account
        )
    ).first()


def retrospect_join_image_find_by(db, retrospect_id, account):
    return db.query(
        Retrospect
    ).options(
        joinedload(Retrospect.image)
    ).filter(
        Retrospect.id == retrospect_id,
        Retrospect.account_id == account
    ).first()


def get_retrospect_list_by(db, account_id, date):
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
