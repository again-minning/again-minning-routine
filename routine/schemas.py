import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, validator

from routine.constants.category import Category
from routine.constants.week import Week


class RoutineCoreBase(BaseModel):
    title: str
    category: Category


class RecommendedRoutineResponse(RoutineCoreBase):
    description: str


class RoutineBase(RoutineCoreBase):
    goal: str
    start_time: str
    days: List[Week] = []


class RoutineCreateRequest(RoutineBase):
    account_id: int

    @validator('start_time')
    def validate_start_time(cls, request):
        regex = re.compile(r'^([0-1]?\d|2[0-3])(?::([0-5]?\d))?(?::([0-5]?\d))?$')
        valid = regex.search(request)
        if valid is None:
            raise ValueError('반드시 start_time 의 형식은 hh:mm:ss 또는 hh:mm 이어야 합니다.')
        return request


class RoutineCommonResponse(RoutineBase):
    routine_id: int
    # result: Result


class RoutineCreateResponse(RoutineCommonResponse):
    pass


class Routine(RoutineBase):
    from retrospect.schemas import Retrospect
    routine_id: int
    account_id: int
    retrospects: List[Retrospect] = []
    is_delete: bool
    created_at: datetime

    class Config:
        orm_mode = True
