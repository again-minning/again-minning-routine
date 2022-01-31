from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form, Header
from sqlalchemy.orm import Session

from base.database.database import get_db
from base.dependencies.header import check_account_header
from base.schemas import SimpleSuccessResponse
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from retrospect.repository.retrospect_repository import create_retrospect
from retrospect.constants.retrospect_message import *
router = APIRouter(prefix='/api/v1/retrospects', tags=['retrospects'], dependencies=[Depends(check_account_header)])


@router.post('', response_model=Response[Message, SimpleSuccessResponse])
def create_retrospect_router(routine_id: int = Form(...),
                             image: Optional[UploadFile] = File(None),
                             title: str = Form(...),
                             content: str = Form(...),
                             date: str = Form(...),
                             db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    account = int(account)
    success = create_retrospect(db=db, routine_id=routine_id, title=title, content=content, date=date, image=image, account=account)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.RETROSPECT_CREATE_OK, msg=RETROSPECT_CREATE_MESSAGE),
        data=SimpleSuccessResponse(success=success))
    return response
