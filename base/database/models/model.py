from sqlalchemy import Column, DateTime, Boolean

from base.utils.time import get_now


class TimestampMixin(object):
    def __init__(self):
        self.created_at = get_now()
        self.modified_at = get_now()
    modified_at = Column(DateTime)
    created_at = Column(DateTime)

    def update_modified_at(self):
        self.modified_at = get_now()


class BaseColumnMixin(object):
    is_delete = Column(Boolean, default=False)
