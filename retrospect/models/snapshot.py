from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from base.database.database import Base
from base.database.models.model import TimestampMixin, BaseColumnMixin


class Snapshot(BaseColumnMixin, TimestampMixin, Base):
    def __init__(self, url):
        super().__init__()
        self.url = url

    __tablename__ = 'snapshots'

    snapshot_id = Column(Integer, primary_key=True)

    retrospect = relationship('Retrospect', back_populates='image')

    retrospect_id = Column(Integer, ForeignKey('retrospects.retrospect_id'))

    url = Column(String)
