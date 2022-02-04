from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship

from base.database.database import Base
from base.database.models.model import TimestampMixin, BaseColumnMixin
from retrospect.models.snapshot import Snapshot


class Retrospect(BaseColumnMixin, TimestampMixin, Base):
    def __init__(self, routine_id: int, account_id: int, title: str, content: str, scheduled_date):
        super().__init__()
        self.routine_id = routine_id
        self.account_id = account_id
        self.title = title
        self.content = content
        self.scheduled_date = scheduled_date

    __tablename__ = 'retrospects'

    __table_args__ = (Index('ix_retrospects_id_account_id', 'account_id', 'retrospect_id'),)

    id = Column('retrospect_id', Integer, primary_key=True)

    account_id = Column(Integer, nullable=False)

    # OneToOne
    image = relationship('Snapshot', back_populates='retrospect', uselist=False)

    routine = relationship('Routine')

    routine_id = Column(Integer, ForeignKey('routine.routine_id'))

    title = Column(String)

    content = Column(Text)

    scheduled_date = Column(DateTime)

    def add_image(self, url):
        self.image = Snapshot(url=url)
