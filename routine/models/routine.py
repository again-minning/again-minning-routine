from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from base.database.database import Base
from routine.constants.category import Category
from routine.models.routineDay import RoutineDay


class Routine(Base):
    __tablename__ = 'routines'

    routine_id = Column(Integer, primary_key=True, index=True)

    account_id = Column(Integer, index=True, nullable=False)

    title = Column(String, nullable=False)

    goal = Column(String, nullable=False)

    category = Column(Enum(Category), nullable=False)

    days = relationship('RoutineDay', back_populates='routine')

    is_delete = Column(Boolean, default=False)

    start_time = Column(Time, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def add_days(self, request_days):
        self.days = [RoutineDay(sequence=0, day=day) for day in request_days]
