from motor.motor_asyncio import AsyncIOMotorClient


async def get_report(mongo_db: AsyncIOMotorClient, date: str, account_id: int):
    report = await mongo_db.reports.find_one({'created_at': date, 'account_id': account_id})
    return report
