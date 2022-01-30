from typing import Optional, List

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from base.database.database import get_db
from base.exception.exception import NotFoundException
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from base.utils.time import validate_date, check_is_modified_period
from routine.constants.routine_message import ROUTINE_CREATE_MESSAGE, ROUTINE_RESULTS_UPDATE_MESSAGE, ROUTINE_GET_MESSAGE, ROUTINE_UPDATE_MESSAGE, ROUTINE_RESULT_CANCEL_MESSAGE, \
    ROUTINE_NO_DATA_RESPONSE
from routine.repository.routine_repository import create_routine, get_routine_list, update_or_create_routine_result, get_routine_detail, patch_routine_detail, cancel_routine_results
from routine.schemas import RoutineCreateRequest, SimpleSuccessResponse, RoutineElementResponse, RoutineResultUpdateRequest, RoutineDetailResponse

router = APIRouter(prefix='/api/v1/routines', tags=['routines'])


@router.get('/account', response_model=Response[Message, Optional[List[RoutineElementResponse]]])
def get_routine_list_router(today: Optional[str], db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    results = get_routine_list(db, int(account), today)
    if results is None:
        raise NotFoundException(name=ROUTINE_NO_DATA_RESPONSE)
    response = Response(
        message=Message(status=HttpStatus.ROUTINE_LIST_OK, msg=ROUTINE_GET_MESSAGE),
        data=RoutineElementResponse.to_list_response(values=results)
    )
    return response


@router.post('', response_model=Response[Message, SimpleSuccessResponse])
def create_routine_router(routine: RoutineCreateRequest, db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    success = create_routine(db, routine, int(account))
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.ROUTINE_CREATE_OK, msg=ROUTINE_CREATE_MESSAGE),
        data=SimpleSuccessResponse(success=success))
    return response


@router.post('/{routine_id}/check-result', response_model=Response[Message, SimpleSuccessResponse])
def update_routine_result_router(routine_id: int, date: str, request: RoutineResultUpdateRequest, db: Session = Depends(get_db)):
    validate_date(date)
    check_is_modified_period(date)
    success = update_or_create_routine_result(db=db, routine_id=routine_id, date=date, reqeust=request)
    response = Response(
        message=Message(status=HttpStatus.ROUTINE_OK, msg=ROUTINE_RESULTS_UPDATE_MESSAGE),
        data=SimpleSuccessResponse(success=success)
    )
    return response


@router.get('/{routine_id}', response_model=Response[Message, RoutineDetailResponse])
def get_routine_detail_router(routine_id: int, db: Session = Depends(get_db)):
    result = get_routine_detail(db=db, routine_id=routine_id)
    if result is None:
        raise NotFoundException(name=ROUTINE_NO_DATA_RESPONSE)
    response = Response[Message, RoutineDetailResponse](
        message=Message(status=HttpStatus.ROUTINE_DETAIL_OK, msg=ROUTINE_GET_MESSAGE),
        data=RoutineDetailResponse.to_response(result=result)
    )
    return response


@router.patch('/{routine_id}', response_model=Response[Message, SimpleSuccessResponse])
def patch_routine_detail_router(routine_id: int, request: RoutineCreateRequest, db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    success = patch_routine_detail(db=db, routine_id=routine_id, request=request, account=int(account))
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.ROUTINE_PATCH_OK, msg=ROUTINE_UPDATE_MESSAGE),
        data=SimpleSuccessResponse(success=success)
    )
    return response


@router.patch('/cancel/{routine_id}', response_model=Response[Message, SimpleSuccessResponse])
def cancel_routine_results_router(routine_id: int, date: str, db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    validate_date(date)
    success = cancel_routine_results(routine_id=routine_id, date=date, db=db)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.ROUTINE_PATCH_OK, msg=ROUTINE_RESULT_CANCEL_MESSAGE),
        data=SimpleSuccessResponse(success=success)
    )
    return response


@router.delete('/{routine_id}', response_model=Response[Message, SimpleSuccessResponse])
def delete_routine_router(routine_id: int, db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    success = delete_routine(routine_id=routine_id, db=db)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.ROUTINE_DELETE_OK, msg=ROUTINE_DELETE_RESPONSE),
        data=SimpleSuccessResponse(success=success)
    )
    return response


@router.patch('/days/sequence', response_model=Response[Message, SimpleSuccessResponse])
def change_routine_sequence_router(date: str, routine_sequences: RoutineSequenceRequest, db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    weekday = convert_str2datetime(date).weekday()
    success = change_routine_sequence(account_id=int(account), weekday=weekday, db=db, routine_sequences=routine_sequences)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.ROUTINE_DELETE_OK, msg=ROUTINE_SEQUENCE_CHANGE_RESPONSE),
        data=SimpleSuccessResponse(success=success)
    )
    return response
