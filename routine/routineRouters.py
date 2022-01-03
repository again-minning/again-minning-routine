from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from base.database.database import get_db
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from routine.repository.routineRepository import create_routine, get_routine
from routine.schemas import RoutineCreateRequest, RoutineCreateResponse

router = APIRouter(prefix='/api/v1/routine', tags=['routines'])


@router.get('/{routine_id}')
def get_routine_router(routine_id: int, db: Session = Depends(get_db)):
    routine = get_routine(db, routine_id)
    return routine


@router.post('/create', response_model=Response[Message, RoutineCreateResponse])
def create_routine_router(routine: RoutineCreateRequest, db: Session = Depends(get_db)):
    save_routine = create_routine(db, routine)
    response = Response[Message, RoutineCreateResponse](
        message=Message(status=HttpStatus.ROUTINE_OK, msg='루틴 생성에 성공하셨습니다.'),
        data=RoutineCreateResponse(routine_id=save_routine.routine_id, success=True)
                        )
    return response
