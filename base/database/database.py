from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings

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
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
