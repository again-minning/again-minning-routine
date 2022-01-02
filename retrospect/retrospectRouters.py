from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from base.database.database import get_db
from retrospect.repository.retrospectRepository import create_retrospect

router = APIRouter(prefix='/api/v1/retrospect', tags=['retrospects'])


@router.post('/create')
def create_retrospect_router(routine_id: str = Form(...),
                             content: str = Form(...),
                             date: str = Form(...),
                             image: UploadFile = File(...),
                             db: Session = Depends(get_db)):
    save_retrospect = create_retrospect(db, routine_id, content, date,  image)
    return save_retrospect
