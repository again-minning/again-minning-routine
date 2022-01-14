import importlib
import os
from pathlib import Path

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from main import app
from base.database.database import SessionLocal, get_db


def override_get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='module')
def client(tmp_path_factory: pytest.TempPathFactory):
    tmp_path = tmp_path_factory.mktemp("data")
    cwd = os.getcwd()
    os.chdir(tmp_path)
    test_db = Path("./test.db")
    if test_db.is_file():  # pragma: nocover
        test_db.unlink()
    # Import while creating the client to create the DB after starting the test session
    import main

    # Ensure import side effects are re-executed
    importlib.reload(main)
    with TestClient(main.app) as c:
        yield c
    if test_db.is_file():  # pragma: nocover
        test_db.unlink()
    os.chdir(cwd)
