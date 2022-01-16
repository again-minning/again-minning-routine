from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from base.database.database import Base
from base.database.models.model import TimestampMixin, BaseColumnMixin
from routine.constants.result import Result


class RoutineResult(BaseColumnMixin, TimestampMixin, Base):

    def __init__(self, week_day: int, yymmdd: str, result: Result = Result.NOT, routine_id: int = None):
        self.yymmdd = yymmdd
        self.week_day = week_day
        self.result = result
        self.routine_id = routine_id

    __tablename__ = 'routine_result'

    id = Column('routine_result_id', Integer, primary_key=True, index=True)

    routine_id = Column(Integer, ForeignKey('routine.routine_id', ondelete='CASCADE'))

    routine = relationship('Routine', back_populates='routine_results')

    week_day = Column(Integer)

    result = Column(Enum(Result), default=Result.NOT)

    yymmdd = Column(DateTime(timezone=True))
