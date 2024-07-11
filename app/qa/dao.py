from sqlalchemy import delete, func, select

from app.dao.dao import BaseDAO
from app.qa.models import QA
from app.settings.db import session_maker


class QaDAO(BaseDAO):
    model = QA

    @classmethod
    def get_stat(cls, user_id):
        with session_maker() as session:
            stmt = select(func.avg(cls.model.mark)).filter_by(user=user_id)
            result = session.execute(stmt)
            return result.mappings().one_or_none()

    @classmethod
    def get_user_marks(cls, user_id):
        with session_maker() as session:
            stmt = select(cls.model.id, cls.model.mark).filter_by(user=user_id)
            result = session.execute(stmt)
            return result.mappings().all()

    @classmethod
    def delete_all_user_marks(cls, user_id):
        with session_maker() as session:
            stmt = delete(cls.model).filter_by(user=user_id)
            session.execute(stmt)
            session.commit()

    @classmethod
    def get_mark_count_and_sum(cls, user_id):
        with session_maker() as session:
            query = select(func.sum(cls.model.mark), func.count(cls.model.mark),
                           func.avg(cls.model.mark)).filter_by(user=user_id)
            result = session.execute(query)
            return result.mappings().one_or_none()
