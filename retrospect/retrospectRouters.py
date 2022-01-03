from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from base.database.database import get_db

router = APIRouter(prefix='/api/v1/retrospect', tags=['retrospects'])


@router.post('/create')
def create_retrospect_router(routine_id: str = Form(...),
                             image: UploadFile = File(...),
                             db: Session = Depends(get_db)):
    pass
