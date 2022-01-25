import re
from typing import List, Optional

from pydantic import BaseModel, validator, root_validator

from routine.constants.category import Category
from routine.constants.result import Result
from routine.constants.routine_message import \
    ROUTINE_FIELD_DAYS_ERROR_MESSAGE, ROUTINE_FIELD_GOAL_ERROR_MESSAGE, ROUTINE_FIELD_TITLE_ERROR_MESSAGE, ROUTINE_FIELD_START_TIME_ERROR_MESSAGE, ROUTINE_FIELD_DATE_ERROR_MESSAGE
from routine.constants.week import Week


class RoutineCoreBase(BaseModel):
    title: str
    category: Category


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


class RoutineCreateResponse(BaseModel):
    routine_id: int
    success: bool


class RoutineElementResponse(BaseModel):
    title: str
    id: int
    goal: str
    start_time: str
    result: str

    @classmethod
    def to_list_response(cls, values):
        routines, today = values
        response = cls.__extract_routine_list_dto(routines, today)
        data = [
            RoutineElementResponse(
                title=routine.title, id=routine.id,
                goal=routine.goal, start_time=str(routine.start_time),
                result=result.upper()
            ) for routine, result in response
        ]
        return data

    @classmethod
    def __extract_routine_list_dto(cls, routines, today):
        response = []
        for routine in routines:
            results = routine.routine_results
            for result in results:
                if result.yymmdd == today:
                    value = result.result
                    break
            else:
                value = 'NOT'
            response.append((routine, value))
        return response


class RoutineResultUpdateRequest(BaseModel):
    result: Result
    date: str

    @validator('date')
    def validate_date(cls, request):
        regex = re.compile(r'^[\d]{4}-[\d]{2}-[\d]{2}$')
        valid = regex.search(request)
        if valid is None:
            raise ValueError(ROUTINE_FIELD_DATE_ERROR_MESSAGE)
        return request


class RoutineDaysResponse(BaseModel):
    routine_id: int
    day: Week


class RoutineDetailResponse(BaseModel):
    id: int
    title: str
    category: Category
    start_time: str
    goal: str
    is_alarm: bool
    days: List[RoutineDaysResponse]

    @classmethod
    def to_response(cls, result):
        res = RoutineDetailResponse(
            id=result.id, title=result.title, category=result.category, start_time= str(result.start_time),
            goal=result.goal, is_alarm=result.is_alarm, days=[RoutineDaysResponse(day=days.day, routine_id=days.routine_id) for days in result.days]
        )
        return res


class SimpleSuccessResponse(BaseModel):
    success: bool
