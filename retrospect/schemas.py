from pydantic import BaseModel

from routine.constants.result import Result


class RetrospectCoreBase(BaseModel):
    content: str


class RetrospectCreateResponse(RetrospectCoreBase):
    from routine.schemas import RoutineCommonResponse
    retrospect_id: int
    date: str
    image: str
    result: Result
    routine: RoutineCommonResponse


class Retrospect(BaseModel):
    pass
