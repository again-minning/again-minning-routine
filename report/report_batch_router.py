from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from base.database.database import get_mongo_db
from report.batch.report_batch import create_weekly_report
from report.schema import CreateReportSchema

router = APIRouter(prefix='/api/v1/batch-reports', tags=['batch-reports'])


@router.post('/week')
async def create_weekly_report_router(data: CreateReportSchema = Body(...), mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)):
    report_id = await create_weekly_report(request=data, mongo_db=mongo_db)
    return report_id
