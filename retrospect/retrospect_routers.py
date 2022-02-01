from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form, Header
from sqlalchemy.orm import Session

from base.database.database import get_db
from base.dependencies.header import check_account_header
from base.schemas import SimpleSuccessResponse
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from retrospect.repository.retrospect_repository import create_retrospect, get_detail_retrospect, put_detail_retrospect
from retrospect.constants.retrospect_message import RETROSPECT_CREATE_MESSAGE, RETROSPECT_DETAIL_MESSAGE, RETROSPECT_UPDATE_MESSAGE
from retrospect.schemas import DetailRetrospectSchema

router = APIRouter(prefix='/api/v1/retrospects', tags=['retrospects'], dependencies=[Depends(check_account_header)])


@router.post('', response_model=Response[Message, SimpleSuccessResponse])
def create_retrospect_router(routine_id: int = Form(...),
                             image: Optional[UploadFile] = File(None),
                             content: str = Form(...),
                             date: str = Form(...),
                             db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    account = int(account)
    success = create_retrospect(db=db, routine_id=routine_id, content=content, date=date, image=image, account=account)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.RETROSPECT_CREATE_OK, msg=RETROSPECT_CREATE_MESSAGE),
        data=SimpleSuccessResponse(success=success))
    return response


@router.get('/{retrospect_id}', response_model=Response[Message, DetailRetrospectSchema])
def get_detail_retrospect_router(retrospect_id: int, db: Session = Depends(get_db)):
    retrospect = get_detail_retrospect(db=db, retrospect_id=retrospect_id)

    response = Response[Message, DetailRetrospectSchema](
        message=Message(status=HttpStatus.RETROSPECT_DETAIL_OK, msg=RETROSPECT_DETAIL_MESSAGE),
        data=DetailRetrospectSchema.to_response(retrospect=retrospect)
    )
    return response


@router.put('/{retrospect_id}', response_model=Response[Message, SimpleSuccessResponse])
def put_detail_retrospect_router(retrospect_id: int,
                                 content: str = Form(...),
                                 image: Optional[UploadFile] = File(None),
                                 db: Session = Depends(get_db)):
    success = put_detail_retrospect(retrospect_id=retrospect_id, content=content, image=image, db=db)
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.RETROSPECT_UPDATE_OK, msg=RETROSPECT_UPDATE_MESSAGE),
        data=SimpleSuccessResponse(success=success))
    return response
