from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from base.database.database import get_db
from routine.repository.routineRepository import create_routine
from routine.schemas import RoutineCreateRequest

router = APIRouter(prefix='/api/v1/routine', tags=['routines'])


@router.get('')
async def get_routine():
    return 'routine'


@router.post('/create')
async def create_routine_router(routine: RoutineCreateRequest, db: Session = Depends(get_db)):
    save_routine = create_routine(db, routine)
    return save_routine
