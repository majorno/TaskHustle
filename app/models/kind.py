from enum import IntEnum, unique
from sqlalchemy import Column, Integer, String
from app.db.core import Base


@unique
class TaskKind(IntEnum):
    REVERSE = 1
    SWAP = 2
    REPEAT = 3


class Kind(Base):
    __tablename__ = 'kind'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=16))
