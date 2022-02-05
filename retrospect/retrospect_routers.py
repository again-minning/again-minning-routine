from typing import Optional, List

from fastapi import APIRouter, Depends, UploadFile, File, Form, Header
from sqlalchemy.orm import Session

from base.database.database import get_db
from base.dependencies.header import check_account_header
from base.schemas import SimpleSuccessResponse
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from base.utils.time import validate_date
from retrospect.service.retrospect_service import (create_retrospect, get_detail_retrospect,
                                                   put_detail_retrospect, delete_detail_retrospect,
                                                   get_list_retrospect)
from retrospect.constants.retrospect_message import (RETROSPECT_CREATE_MESSAGE, RETROSPECT_DETAIL_MESSAGE,
                                                     RETROSPECT_UPDATE_MESSAGE, RETROSPECT_DELETE_MESSAGE,
                                                     RETROSPECT_LIST_MESSAGE)
from retrospect.schemas import RetrospectResponseSchema

router = APIRouter(prefix='/api/v1/retrospects', tags=['retrospects'], dependencies=[Depends(check_account_header)])


@router.post('', response_model=Response[Message, SimpleSuccessResponse])
def create_retrospect_router(routine_id: int = Form(...),
                             image: Optional[UploadFile] = File(None),
                             content: str = Form(...),
                             date: str = Form(...),
                             db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    success = create_retrospect(db=db, routine_id=routine_id, content=content, date=date, image=image, account=int(account))
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.RETROSPECT_CREATE_OK, msg=RETROSPECT_CREATE_MESSAGE),
        data=SimpleSuccessResponse(success=success))
    return response


@router.get('/{retrospect_id}', response_model=Response[Message, RetrospectResponseSchema])
def get_detail_retrospect_router(retrospect_id: int, db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    retrospect = get_detail_retrospect(db=db, retrospect_id=retrospect_id, account=int(account))

    response = Response[Message, RetrospectResponseSchema](
        message=Message(status=HttpStatus.RETROSPECT_DETAIL_OK, msg=RETROSPECT_DETAIL_MESSAGE),
        data=RetrospectResponseSchema.to_response(retrospect=retrospect)
    )
    return response


@router.put('/{retrospect_id}', response_model=Response[Message, SimpleSuccessResponse])
def put_detail_retrospect_router(retrospect_id: int,
                                 content: str = Form(...),
                                 image: Optional[UploadFile] = File(None),
                                 db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    success = put_detail_retrospect(retrospect_id=retrospect_id, content=content, image=image, db=db, account=int(account))
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.RETROSPECT_UPDATE_OK, msg=RETROSPECT_UPDATE_MESSAGE),
        data=SimpleSuccessResponse(success=success))
    return response


@router.delete('/{retrospect_id}', response_model=Response[Message, SimpleSuccessResponse])
def delete_detail_retrospect_router(retrospect_id: int, db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    success = delete_detail_retrospect(db=db, retrospect_id=retrospect_id, account=int(account))
    response = Response[Message, SimpleSuccessResponse](
        message=Message(status=HttpStatus.RETROSPECT_DELETE_OK, msg=RETROSPECT_DELETE_MESSAGE),
        data=SimpleSuccessResponse(success=success))
    return response


@router.get('', response_model=Response[Message, Optional[List[RetrospectResponseSchema]]])
def get_list_retrospect_router(date: str, db: Session = Depends(get_db), account: Optional[str] = Header(None)):
    validate_date(date)
    retrospects = get_list_retrospect(date=date, db=db, account_id=int(account))
    response = Response(
        message=Message(status=HttpStatus.RETROSPECT_LIST_OK, msg=RETROSPECT_LIST_MESSAGE),
        data=RetrospectResponseSchema.to_list_response(retrospects=retrospects)
    )
    return response
