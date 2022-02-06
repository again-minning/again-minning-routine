from sqlalchemy import Column, DateTime, Boolean

from base.utils.time import get_now


class TimestampMixin(object):
    def __init__(self):
        self.created_at = get_now()
        self.modified_at = get_now()
    modified_at = Column(DateTime, onupdate=get_now())
    created_at = Column(DateTime)


class BaseColumnMixin(object):
    is_delete = Column(Boolean, default=False)
