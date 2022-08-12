from enum import IntEnum, unique
from sqlalchemy import Column, Integer, String
from app.db.core import Base


@unique
class TaskStatus(IntEnum):
    PENDING = 1
    PROCESSING = 2
    COMPLETE = 3


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=16))
