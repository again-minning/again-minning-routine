from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from base.database.database import get_db
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from routine.repository.routineRepository import create_routine, get_routine_list, update_or_create_routine_result
from routine.schemas import RoutineCreateRequest, SimpleSuccessResponse, RoutineElementResponse, RoutineResultUpdateRequest

router = APIRouter(prefix='/api/v1/routine', tags=['routines'])


@router.get('/account/{account_id}', response_model=Response[Message, Optional[List[RoutineElementResponse]]])
def get_routine_list_router(account_id: int, today: Optional[str], db: Session = Depends(get_db)):
    routines = get_routine_list(db, account_id, today)
    data = [
        RoutineElementResponse(
            title=routine.title, id=routine.id,
            goal=routine.goal, start_time=str(routine.start_time),
            result=result.upper()
        ) for routine, result in routines
    ]
    response = Response(
        message=Message(status=HttpStatus.ROUTINE_LIST_OK, msg='루틴 조회에 성공하셨습니다.'),
        data=data
    )
    return response


@router.post('', response_model=Response[Message, SimpleSuccessResponse])
def create_routine_router(routine: RoutineCreateRequest, db: Session = Depends(get_db)):
    success = create_routine(db, routine)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.ROUTINE_CREATE_OK, msg='루틴 생성에 성공하셨습니다.'),
        data=SimpleSuccessResponse(success=success))
    return response


@router.put('/{routine_id}', response_model=Response[Message, SimpleSuccessResponse])
def update_routine_result_router(routine_id: int, request: RoutineResultUpdateRequest, db: Session = Depends(get_db)):
    success = update_or_create_routine_result(db=db, routine_id=routine_id, reqeust=request)
    response = Response(
        message=Message(status=HttpStatus.ROUTINE_OK, msg='루틴 결과 업데이트에 성공했습니다.'),
        data=SimpleSuccessResponse(success=success)
    )
    return response
