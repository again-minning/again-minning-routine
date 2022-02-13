from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from base.database.database import get_db
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from routine.constants.routine_message import ROUTINE_GET_MESSAGE
from routine.schemas import RoutineCountResponse, RoutineBatchSchema, RoutineResultSchema
from routine.repository.routine_batch_repository import get_routine_count, get_routine_pagination, get_routine_results_search_in

router = APIRouter(prefix='/api/v1/batch-routines', tags=['batch-routines'])


@router.get('/count', response_model=Response[Message, RoutineCountResponse])
def get_batch_routine_count_router(db: Session = Depends(get_db)):
    routine_counts = get_routine_count(db=db)
    return Response(
        message=Message(status=HttpStatus.ROUTINE_OK, msg=ROUTINE_GET_MESSAGE),
        data=RoutineCountResponse.to_response(routine_counts)
    )


@router.get('', response_model=Response[Message, List[RoutineBatchSchema]])
def get_batch_routine_list_router(limit: int, offset: int, db: Session = Depends(get_db)):
    routines = get_routine_pagination(db=db, limit=limit, offset=offset)
    return Response(
        message=Message(status=HttpStatus.ROUTINE_LIST_OK, msg=ROUTINE_GET_MESSAGE),
        data=RoutineBatchSchema.to_list_response(routines)
    )


@router.get('/results', response_model=Response[Message, List[RoutineResultSchema]])
def get_batch_routine_results_router(start_date: str = Query(..., alias='start-date'), end_date: str = Query(..., alias='end-date'),
                                     routine_ids: list = Query(..., alias='routine-ids'), db: Session = Depends(get_db)):
    routine_results = get_routine_results_search_in(db=db, start_date=start_date, end_date=end_date, routine_ids=routine_ids)
    return Response(
        message=Message(status=HttpStatus.ROUTINE_LIST_OK, msg=ROUTINE_GET_MESSAGE),
        data=RoutineResultSchema.to_list_response(routine_results)
    )
