import asyncio
from typing import Generator

import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from base.database.connection import models
from base.database.database import SessionLocal, get_db, conn
from config.settings import settings
from main import app
from report.collections import Collections


@pytest.fixture(scope='function')
def db() -> Generator:
    db: Session = SessionLocal()
    try:
        yield db
        db.rollback()
    finally:
        db.close()


def override_get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except HTTPException:
        db.rollback()
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client() -> Generator:
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        yield client


@pytest.fixture(scope='function')
async def mongo_db() -> Generator:
    db = conn
    db.client = AsyncIOMotorClient(settings.MONGO_URL)
    try:
        yield db.client
    finally:
        db.client.close()


def maintain_idempotent(func):
    def inner(db: Session, client: TestClient):
        try:
            ret = func(db, client)
        finally:
            for model in models:
                db.query(model).delete()
            db.commit()
        return ret
    return inner


def maintain_idempotent_async():
    def wrapper(func):
        @pytest.mark.parametrize('anyio_backend', ['asyncio'])
        async def inner(anyio_backend, async_client: AsyncClient, mongo_db: AsyncIOMotorClient):
            try:
                ret = await func(anyio_backend, async_client, mongo_db)
            finally:
                collections = [Collections.REPORT.value, Collections.MONTHLY_REPORT.value]
                for collection in collections:
                    await mongo_db[settings.DB_NAME][collection].delete_many({})
            return ret
        return inner
    return wrapper

