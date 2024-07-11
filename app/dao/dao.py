
from sqlalchemy import delete, insert, select

from app.settings.db import session_maker


class BaseDAO:
    model = None

    @classmethod
    def select_all_filter(cls, filter_by):
        with session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = session.execute(query)
            return result.mappings().all()

    @classmethod
    def select_all(cls):
        with session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = session.execute(query)
            return result.mappings().all()

    @classmethod
    def add(cls, data):
        with session_maker() as session:
            stmt = insert(cls.model).values(**data)
            session.execute(stmt)
            session.commit()

    @classmethod
    def delete(cls, id):
        with session_maker() as session:
            stmt = delete(cls.model).filter_by(id=id)
            session.execute(stmt)
            session.commit()