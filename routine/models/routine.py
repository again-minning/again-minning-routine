from sqlalchemy import Column, Integer, String, Enum, Time, Boolean
from sqlalchemy.orm import relationship, Session

from base.database.database import Base
from base.database.models.model import TimestampMixin, BaseColumnMixin
from base.utils.time import get_now, convert_str2date, convert_str2time
from routine.constants.category import Category
from routine.constants.result import Result
from routine.constants.week import Week
from routine.models.routineDay import RoutineDay
from routine.models.routineResult import RoutineResult
from routine.schemas import RoutineCreateRequest


class Routine(BaseColumnMixin, TimestampMixin, Base):

    def __init__(self, account_id, title, goal, category, start_time, is_alarm=False):
        super().__init__()
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

    def init_days(self, request_days):
        self.days = [RoutineDay(sequence=0, day=day) for day in request_days]

    def add_days(self, request_days):
        self.days += [RoutineDay(sequence=0, day=day) for day in request_days]

    def patch_days(self, db: Session, request_days):
        days = self.days
        deleted = []
        retained = set()
        for day in days:
            if day.day not in request_days:
                deleted.append(day)
            else:
                retained.add(day.day)
        added = request_days - retained
        self.add_days(added)
        self.delete_days(db, deleted)
        self.update_modified_at()

    def delete_days(self, db, deleted):
        for delete_day in deleted:
            db.delete(delete_day)

    def init_set_routine_result(self, request_days):
        now = get_now()
        weekday = now.weekday()
        date = convert_str2date(str(now))
        routine_result = []
        if Week.get_weekday(weekday) in request_days:
            routine_result.append(RoutineResult(yymmdd=date, result=Result.NOT))
        self.routine_results = routine_result

    def update_routine(self, request: RoutineCreateRequest):
        self.title = request.title
        self.category = request.category
        self.start_time = convert_str2time(request.start_time)
        self.goal = request.goal
        self.is_alarm = request.is_alarm
        self.update_modified_at()
