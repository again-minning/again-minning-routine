from typing import Optional, List, Dict

from bson import ObjectId
from pydantic import BaseModel, Field

from routine.constants.category import Category
from routine.schemas import RoutineBatchSchema, RoutineResultSchema


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class RoutineResultElement(BaseModel):
    date: str
    result: str


class RoutineElement(BaseModel):
    routine_id: int
    title: str
    category: Category
    results: List[RoutineResultElement]


class CategoryRoutineElement(BaseModel):
    title: str
    done_count: int
    try_count: int
    not_count: int


class MonthlyReport(BaseModel):
    """
    지난 4주치의 주말 리포트를 요약해주는 리포트
    즉 n주차, n-1주차, n-2주차, n-3주차의 리포트를 요약해줘서 보여주는 리포트
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    account_id: int
    weekly_achievement_rate: List[float]
    category_routine_count: Dict[str, int]
    category_detail: Dict[str, Dict[str, CategoryRoutineElement]]
    created_at: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            'example': {
                'account_id': 1,
                'weekly_achievement_rate': [80, 42, 100, 90],
                'category_routine_count': {
                    'MIRACLE': 3,
                    'SELF': 2,
                    'HEALTH': 1,
                    'DAILY': 1,
                    'ETC': 1,
                },
                'category_detail': {
                    'MIRACLE': {
                        1: {
                            'title': 'i can do it',
                            'done_count': 9,
                            'try_count': 1,
                            'not_count': 2
                        },
                        2: {
                            'title': 'i can do it',
                            'done_count': 9,
                            'try_count': 1,
                            'not_count': 2
                        }
                    },
                    'SELF': {
                        ...
                    }
                }
            }
        }


class Report(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    account_id: int
    achievement_rate: float
    done_count: int
    try_count: int
    not_count: int
    routine_results: Optional[List[RoutineElement]]
    created_at: str

    @classmethod
    def calculate_achievement_rate(cls, _done, _try, _none):
        return (_done + 0.5 * _try) / (_none + _try + _done)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            'example': {
                'account_id': 1,
                'achievement_rate': 70,
                'done_count': 6,
                'try_count': 2,
                'not_count': 2,
                'routine_results': [
                    {
                        'routine_id': 1,
                        'title': 'first',
                        'category': 'SELF',
                        'results': [
                            {
                                'date': '2022-02-01',
                                'result': 'DONE'
                            },
                            {
                                'date': '2022-02-03',
                                'result': 'TRY'
                            }
                        ]
                    },
                    {
                        'routine_id': 2,
                        'title': 'second',
                        'category': 'HEALTH',
                        'results': [
                            {
                                'date': '2022-02-01',
                                'result': 'DONE'
                            },
                            {
                                'date': '2022-02-03',
                                'result': 'TRY'
                            }
                        ]
                    }
                ]
            }
        }


class CreateReportSchema(BaseModel):
    routines: List[RoutineBatchSchema]
    routine_results: List[RoutineResultSchema]
