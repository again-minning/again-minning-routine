from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from base.database.database import Base
from base.database.models.model import TimestampMixin, BaseColumnMixin
from routine.constants.result import Result


class RoutineResult(BaseColumnMixin, TimestampMixin, Base):

    def __init__(self, yymmdd: str, result: Result = Result.NOT, routine_id: int = None):
        super().__init__()
        self.yymmdd = yymmdd
        self.result = result
        self.routine_id = routine_id

    __tablename__ = 'routine_result'

    id = Column('routine_result_id', Integer, primary_key=True)

    routine_id = Column(Integer, ForeignKey('routine.routine_id', ondelete='CASCADE'))

    routine = relationship('Routine', back_populates='routine_results')

    result = Column(Enum(Result), default=Result.NOT)

    yymmdd = Column(DateTime)

    def update_result(self, result):
        self.result = result
