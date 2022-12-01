from .db_conn import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import Optional, List
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, Integer, Column, Float, Date
from sqlalchemy.sql.expression import text, func
# from sqlalchemy.sql.schema import Column


class User(Base):
    """
    [summary]: Table structure for user class
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    mobile = Column(String, unique=True, nullable=False)
    # joined_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
    joined_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())
    # Date of birth


class Profile(Base):
    """
    [summary]: Table structure for user profile
    Name:
    Team Name:
    Player since:
    Mobile: from User table
    Email: from User table
    Address:
    """

    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, nullable=False)
    team_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class Auth(Base):
    """
    [summary]: table structure for authentication, used for validation of OTP
    """

    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    otp = Column(Integer, nullable=False)
    # expiry = Column(TIMESTAMP(timezone=True), nullable=False)
    # attempts_so_far = Column(Integer, nullable=False)
