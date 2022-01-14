from sqlalchemy import Column, Integer, String, Enum, Time, Boolean
from sqlalchemy.orm import relationship

from base.database.database import Base
from base.database.models.model import TimestampMixin, BaseColumnMixin
from base.utils.time import get_now, convert_str2date, default_date
from routine.constants.category import Category
from routine.constants.result import Result
from routine.constants.week import Week
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult


class Routine(BaseColumnMixin, TimestampMixin, Base):

    def __init__(self, account_id, title, goal, category, start_time, is_alarm=False):
        self.account_id = account_id
        self.title = title
        self.goal = goal
        self.category = category
        self.start_time = start_time
        self.is_alarm = is_alarm

    __tablename__ = 'routine'

    id = Column('routine_id', Integer, primary_key=True, index=True)

    account_id = Column(Integer, index=True, nullable=False)

    routine_results = relationship('RoutineResult', back_populates='routine', cascade='all, delete-orphan')

    days = relationship('RoutineDay', back_populates='routine', cascade='all, delete-orphan')

    title = Column(String, nullable=False)

    goal = Column(String, nullable=False)

    category = Column(Enum(Category), nullable=False)

    is_alarm = Column(Boolean, default=False)

    start_time = Column(Time, nullable=False)

    def add_days(self, request_days):
        self.days = [RoutineDay(sequence=0, day=day) for day in request_days]

        now = get_now()
        weekday = now.weekday()
        date = convert_str2date(str(now))
        routine_result = []
        if Week.get_weekday(weekday) in request_days:
            routine_result.append(RoutineResult(week_day=weekday, yymmdd=date, result=Result.NOT))
        else:
            routine_result.append(RoutineResult(week_day=-1, yymmdd=default_date(), result=Result.DEFAULT))
        self.routine_results = routine_result
