from sqlalchemy import Column, DateTime, func, Boolean


class TimestampMixin(object):
    modified_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())


class BaseColumnMixin(object):
    is_delete = Column(Boolean, default=False)
