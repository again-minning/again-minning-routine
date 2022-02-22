from motor.motor_asyncio import AsyncIOMotorClient

from base.exception.exception import MinningException
from base.utils.time import convert_str2datetime, get_start_datetime, get_end_datetime
from config.settings import settings
from report.collections import Collections
from report.constants.report_message import REPORT_NOT_FOUND


async def get_report(mongo_db: AsyncIOMotorClient, date: str, account_id: int):
    start_today = get_start_datetime(convert_str2datetime(date)).strftime('%Y-%m-%dT%H:%M:%S')
    end_today = get_end_datetime(convert_str2datetime(date)).strftime('%Y-%m-%dT%H:%M:%S')
    report = await mongo_db[settings.DB_NAME][Collections.REPORT].find_one(
        {
            'created_at': {
                '$gte': start_today, '$lte': end_today
            },
            'account_id': account_id
        }, {
            '_id': 0
        }
    )
    if not report:
        raise MinningException(REPORT_NOT_FOUND)
    return report


async def get_monthly_report(mongo_db: AsyncIOMotorClient, date: str, account_id: int):
    start_today = get_start_datetime(convert_str2datetime(date)).strftime('%Y-%m-%dT%H:%M:%S')
    end_today = get_end_datetime(convert_str2datetime(date)).strftime('%Y-%m-%dT%H:%M:%S')
    report = await mongo_db[settings.DB_NAME][Collections.MONTHLY_REPORT].find_one(
        {
            'created_at': {
                '$gte': start_today, '$lte': end_today
            },
            'account_id': account_id
        }, {
            '_id': 0
        }
    )
    if not report:
        raise MinningException(REPORT_NOT_FOUND)
    return report
