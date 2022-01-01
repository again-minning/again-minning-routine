from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from base.database.database import Base
from routine.constants.week import Week


class RoutineDay(Base):
    __tablename__ = 'routine_days'

    routine_day_id = Column(Integer, primary_key=True, index=True)

    day = Column(Enum(Week))

    sequence = Column(Integer)

    routine = relationship('Routine', back_populates='days')

    routine_id = Column(Integer, ForeignKey('routines.routine_id'))

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
