from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from base.database.database import Base
from retrospect.models.snapshot import Snapshot
from routine.constants.result import Result


class Retrospect(Base):
    __tablename__ = 'retrospects'

    retrospect_id = Column(Integer, primary_key=True, index=True)

    # OneToOne
    image = relationship('Snapshot', back_populates='retrospect', uselist=False)

    # ManyToOne
    routine = relationship('Routine', back_populates='retrospects')

    routine_id = Column(Integer, ForeignKey('routines.routine_id'))

    content = Column(String)

    result = Column(Enum(Result))

    is_report = Column(Boolean, default=False)

    date = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def add_image(self, url):
        self.image = Snapshot(url=url)
