import logging

from motor.motor_asyncio import AsyncIOMotorClient

from base.database.database import conn
from config.settings import settings


async def connect_to_mongo():
    logging.info('Connecting to database...')
    conn.client = AsyncIOMotorClient(settings.MONGO_URL, maxPoolSize=10, minPoolSize=10)
    logging.info('MongoDB Connected!')


async def close_mongo_connection():
    logging.info('Closing MongDB Connection')
    conn.client.close()
    logging.info('MongDB Closed')
