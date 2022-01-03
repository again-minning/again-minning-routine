from fastapi import UploadFile
from sqlalchemy.orm import Session


def create_retrospect(db: Session, routine_id: str , image: UploadFile):
    pass
