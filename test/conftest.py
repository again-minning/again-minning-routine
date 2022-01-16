from typing import Generator

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from base.database.connection import models
from base.database.database import SessionLocal, get_db
from main import app


@pytest.fixture(scope='function')
def db() -> Generator:
    db: Session = SessionLocal()
    yield db
    db.rollback()
    db.close()


def override_get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except HTTPException as e:
        db.rollback()
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as c:
        yield c


def complex_transaction(func):
    def inner(db: Session, client: TestClient):
        ret = func(db, client)
        for model in models:
            db.query(model).delete()
        db.commit()
        return ret
    return inner
