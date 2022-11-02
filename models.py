from db_conn import Base
from typing import Optional, List
from uuid import UUID, uuid4
from sqlalchemy import String, Integer, Column


class User(Base):
    __tablename__ = 'test_user_tbl'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
