from typing import Optional

from fastapi import APIRouter, Depends, Header
from motor.motor_asyncio import AsyncIOMotorClient

from base.database.database import get_mongo_db
from base.dependencies.header import check_account_header
from base.utils.constants import HttpStatus
from base.utils.message import Response, Message
from report.constants.report_message import REPORT_GET_OK
from report.repository.report_repository import get_report, get_monthly_report
from report.schema import Report, MonthlyReport

router = APIRouter(prefix='/api/v1/reports', tags=['reports'], dependencies=[Depends(check_account_header)])


@router.get('/week', response_model=Response[Message, Report])
async def get_weekly_report_router(date: Optional[str], account: Optional[str] = Header(None), mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)):
    report = await get_report(mongo_db=mongo_db, date=date, account_id=int(account))
    response = Response(
        message=Message(status=HttpStatus.REPORT_DETAIL_OK, msg=REPORT_GET_OK),
        data=report
    )
    return response


@router.get('/month', response_model=Response[Message, MonthlyReport])
async def get_monthly_report_router(date: Optional[str], account: Optional[str] = Header(None), mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)):
    report = await get_monthly_report(mongo_db=mongo_db, date=date, account_id=int(account))
    response = Response(
        message=Message(status=HttpStatus.REPORT_DETAIL_OK, msg=REPORT_GET_OK),
        data=report
    )
    return response
