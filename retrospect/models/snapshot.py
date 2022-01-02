from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from base.database.database import Base


class Snapshot(Base):
    __tablename__ = 'snapshots'

    snapshot_id = Column(Integer, primary_key=True, index=True)

    retrospect = relationship('Retrospect', back_populates='image')

    retrospect_id = Column(Integer, ForeignKey('retrospects.retrospect_id'))

    url = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
