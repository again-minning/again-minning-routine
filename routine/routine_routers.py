from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from base.database.database import get_db
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from routine.constants.routine_message import ROUTINE_CREATE_MESSAGE, ROUTINE_RESULTS_UPDATE_MESSAGE, ROUTINE_GET_MESSAGE, ROUTINE_UPDATE_MESSAGE
from routine.repository.routine_repository import create_routine, get_routine_list, update_or_create_routine_result, get_routine_detail, patch_routine_detail
from routine.schemas import RoutineCreateRequest, SimpleSuccessResponse, RoutineElementResponse, RoutineResultUpdateRequest, RoutineDetailResponse

router = APIRouter(prefix='/api/v1/routines', tags=['routines'])


@router.get('/account/{account_id}', response_model=Response[Message, Optional[List[RoutineElementResponse]]])
def get_routine_list_router(account_id: int, today: Optional[str], db: Session = Depends(get_db)):
    routines = get_routine_list(db, account_id, today)
    response = Response(
        message=Message(status=HttpStatus.ROUTINE_LIST_OK, msg=ROUTINE_GET_MESSAGE),
        data=RoutineElementResponse.to_list_response(routines=routines)
    )
    return response


@router.post('', response_model=Response[Message, SimpleSuccessResponse])
def create_routine_router(routine: RoutineCreateRequest, db: Session = Depends(get_db)):
    success = create_routine(db, routine)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.ROUTINE_CREATE_OK, msg=ROUTINE_CREATE_MESSAGE),
        data=SimpleSuccessResponse(success=success))
    return response


@router.post('/{routine_id}/check-result', response_model=Response[Message, SimpleSuccessResponse])
def update_routine_result_router(routine_id: int, request: RoutineResultUpdateRequest, db: Session = Depends(get_db)):
    success = update_or_create_routine_result(db=db, routine_id=routine_id, reqeust=request)
    response = Response(
        message=Message(status=HttpStatus.ROUTINE_OK, msg=ROUTINE_RESULTS_UPDATE_MESSAGE),
        data=SimpleSuccessResponse(success=success)
    )
    return response


@router.get('/{routine_id}', response_model=Response[Message, RoutineDetailResponse])
def get_routine_detail_router(routine_id: int, db: Session = Depends(get_db)):
    result = get_routine_detail(db=db, routine_id=routine_id)
    response = Response[Message, RoutineDetailResponse](
        message=Message(status=HttpStatus.ROUTINE_DETAIL_OK, msg=ROUTINE_GET_MESSAGE),
        data=RoutineDetailResponse.to_response(result=result)
    )
    return response


@router.patch('/{routine_id}', response_model=Response[Message, SimpleSuccessResponse])
def patch_routine_detail_router(routine_id: int, request: RoutineCreateRequest, db: Session = Depends(get_db)):
    success = patch_routine_detail(db=db, routine_id=routine_id, request=request)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.ROUTINE_PATCH_OK, msg=ROUTINE_UPDATE_MESSAGE),
        data=SimpleSuccessResponse(success=success)
    )
    return response
