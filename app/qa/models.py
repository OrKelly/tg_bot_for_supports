from sqlalchemy import Column, Integer
from sqlalchemy.orm import validates

from app.settings.db import Base


class QA(Base):
    __tablename__ = 'qa'

    mark = Column(Integer, nullable=False)
    user = Column(Integer)

    @validates('mark')
    def validate_mark(self, key, value):
        assert 0 <= value <= 100
        return value
