from fastapi import UploadFile
from sqlalchemy.orm import Session

from base.utils.time import convert_str2date
from retrospect.models.retrospect import Retrospect
from routine.constants.result import Result


def create_retrospect(db: Session, routine_id: str , content: str, date: str, image: UploadFile):
    date = convert_str2date(date)
    db_retrospect = Retrospect(routine_id=routine_id,
                               content=content,
                               date=date,
                               result=Result.NOT, is_report=False)
    # TODO: 이미지 url은 추후에 변경
    db_retrospect.add_image(image.filename)
    db.add(db_retrospect)
    db.commit()
    db.refresh(db_retrospect)
    return db_retrospect
