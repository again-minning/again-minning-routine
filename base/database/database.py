from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config.settings import settings

# SQLALCHEMY
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
SHOW_SQL = settings.SHOW_SQL
kwargs = {}

if settings.APP_ENV == 'test':
    kwargs['connect_args'] = {
        'check_same_thread': False
    }

# echo = show_sql
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=SHOW_SQL, **kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def commit(func):
    def inner(db: Session, **kwargs):
        try:
            ret = func(db, **kwargs)
            db.commit()
        except Exception:
            db.rollback()
            raise
        return ret

    return inner


# MONGODB
class MongoDB:
    client: AsyncIOMotorClient = None


conn = MongoDB()


async def get_mongo_db() -> AsyncIOMotorClient:
    yield conn.client
