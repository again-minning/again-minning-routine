import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator, root_validator

from routine.constants.category import Category
from routine.constants.result import Result
from routine.constants.week import Week
from routine.constants.routine_message import \
    ROUTINE_FIELD_DAYS_ERROR_MESSAGE, ROUTINE_FIELD_GOAL_ERROR_MESSAGE, ROUTINE_FIELD_TITLE_ERROR_MESSAGE, ROUTINE_FIELD_START_TIME_ERROR_MESSAGE


class SimpleSuccessResponse(BaseModel):
    success: bool


class RoutineCoreBase(BaseModel):
    title: str
    category: Category


class RecommendedRoutineResponse(RoutineCoreBase):
    description: str


class RoutineBase(RoutineCoreBase):
    goal: str
    start_time: str
    days: List[Week] = []

    @validator('goal')
    def validate_goal(cls, request):
        if not request:
            raise ValueError(ROUTINE_FIELD_GOAL_ERROR_MESSAGE)
        return request

    @validator('title')
    def validate_title(cls, request):
        if not request:
            raise ValueError(ROUTINE_FIELD_TITLE_ERROR_MESSAGE)
        return request


class RoutineCreateRequest(RoutineBase):
    account_id: int
    is_alarm: Optional[bool] = False

    @root_validator
    def validate_days(cls, values):
        days = values.get('days', None)
        if not days:
            raise ValueError(ROUTINE_FIELD_DAYS_ERROR_MESSAGE)
        return values

    @validator('start_time')
    def validate_start_time(cls, request):
        regex = re.compile(r'^([0-1]?\d|2[0-3])(?::([0-5]?\d))?(?::([0-5]?\d))?$')
        valid = regex.search(request)
        if valid is None:
            raise ValueError(ROUTINE_FIELD_START_TIME_ERROR_MESSAGE)
        return request


class RoutineElementResponse(BaseModel):
    title: str
    id: int
    goal: str
    start_time: str
    result: str


class RoutineCommonResponse(RoutineBase):
    pass


class RoutineCreateResponse(BaseModel):
    routine_id: int
    success: bool


class Routine(RoutineBase):
    routine_id: int
    account_id: int
    is_delete: bool
    created_at: datetime

    class Config:
        orm_mode = True


class RoutineResultUpdateRequest(BaseModel):
    result: Result
    weekday: Week
    date: str
