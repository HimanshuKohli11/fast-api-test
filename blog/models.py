from .db_conn import Base
# from typing import Optional, List
# from uuid import UUID, uuid4
from sqlalchemy import String, Integer, Column


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
