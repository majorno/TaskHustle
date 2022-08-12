from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.core import Base
from app.models.kind import Kind
from app.models.status import TaskStatus


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    status_id = Column(Integer, ForeignKey('status.id'), default=int(TaskStatus.PENDING))
    kind_id = Column(Integer, ForeignKey(Kind.id))
    data = Column(String())
    result = Column(String())
    status = relationship('Status', lazy='joined')
