from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from base.database.database import Base
from base.database.models.model import TimestampMixin
from routine.constants.week import Week


class RoutineDay(TimestampMixin, Base):

    def __init__(self, sequence, day):
        self.day = day
        self.sequence = sequence

    __tablename__ = 'routine_day'

    day = Column(Enum(Week), primary_key=True)

    routine = relationship('Routine', back_populates='days')

    routine_id = Column(Integer, ForeignKey('routine.routine_id', ondelete='CASCADE'), primary_key=True)

    sequence = Column(Integer)
