from .db_conn import Base
from typing import Optional, List
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, Integer, Column, Float, Date
from sqlalchemy.sql.expression import text, func
from sqlalchemy_utils import UUIDType, URLType
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
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
    enable_status = Column(Integer, nullable=False, default=0)
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


def generate_uuid():
    return str(uuid4())


class PlayerCategory(Base):
    """
    [summary]: Table structure for player category class
    """
    __tablename__ = 'player_category'

    category_id = Column(Integer, primary_key=True, nullable=False)
    # category_id = Column(String, name="uuid", primary_key=True, nullable=False, default=generate_uuid)
    # category_id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    field = Column(String, nullable=False)
    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class Player(Base):
    """
    [summary]: Table structure for player class
    """
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, nullable=False)
    player_name = Column(String, nullable=False)
    player_category = Column(Integer, ForeignKey("player_category.category_id", ondelete="CASCADE"), nullable=False)
    # player_stats = Column(String, ForeignKey("player_stats.id", ondelete="CASCADE"), nullable=False)  # TODO: check
    joined_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())

    image = Column(URLType)

    stats = relationship('PlayerStats', back_populates="player")


class PlayerStats(Base):
    """
    [summary]: Table structure for player stats class
    """
    __tablename__ = 'player_stats'

    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    score = Column(Float, nullable=False)
    achievements = Column(String, nullable=False)
    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())

    player = relationship('Player', back_populates="stats")


class Games(Base):
    """
    [summary]: Table structure for Games class
    """
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, nullable=False)
    # prize = Column(Integer, ForeignKey("prize.id", ondelete="CASCADE"), nullable=False, index=True)
    date_of_play = Column(Date, nullable=False)
    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class Teams(Base):
    """
    [summary]: Table structure for Teams class
    """
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, nullable=False)
    team_name = Column(String, nullable=False)  # TODO: doubt [only one team name per customer??]
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # team_name = Column(String, ForeignKey("profiles.team_name"), nullable=False, index=True)
    player_id_1 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_2 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_3 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_4 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_5 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_6 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_7 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_8 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_9 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_10 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_11 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_12 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id_13 = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    last_submitted_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())
    # game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)  # TODO: resolve race around
    score = Column(Float, nullable=False, default=0)
    # prize_amount = Column(Integer, ForeignKey("prize.prize_amount", ondelete="CASCADE"), nullable=False, index=True)
    rank = Column(Integer, nullable=False, default=-1)
    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class Prizes(Base):
    """
        [summary]: Table structure for Prizes class
        """
    __tablename__ = 'prizes'

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(String, nullable=False)
    image = Column(URLType)
    valid_till = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())
    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class Results(Base):
    """
            [summary]: Table structure for Daily Live Results class
            """
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False, default=0)
    rank = Column(Integer, nullable=False, default=-1)

    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class ResultsDailyLive(Base):
    """
    [summary]: Table structure for Daily Live Results class
    """
    __tablename__ = 'results_daily_live'

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False, index=True)
    start_score = Column(Integer, nullable=False, default=0)
    latest_score = Column(Float, nullable=False, default=0)
    moat_score = Column(Float, nullable=False, default=0)

    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class TransactionTypes(Base):
    """
    [summary]: Table structure for Transaction type
    """
    __tablename__ = 'transaction_type'

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)

    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class DailyTransactions(Base):
    """
    [summary]: Table structure for Transaction type
    """
    __tablename__ = 'daily_transactions'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    transaction_id = Column(Integer, primary_key=True, nullable=False)
    # transaction_id = Column(String, name="uuid", primary_key=True, nullable=False, default=generate_uuid)
    transaction_type = Column(Integer, ForeignKey("transaction_type.id", ondelete="CASCADE"), nullable=False)
    value = Column(Float, nullable=False, default=0)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())

    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class Wallet(Base):
    """
    [summary]: Table structure for Transaction type
    """
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    net_value = Column(Float, nullable=False, default=0)

    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())


class WalletTransactions(Base):
    """
    [summary]: Table structure for Transaction type
    """
    __tablename__ = 'wallet_transactions'

    id = Column(Integer, primary_key=True, nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallet.id", ondelete="CASCADE"), nullable=False)
    transaction_type = Column(Integer, ForeignKey("transaction_type.id", ondelete="CASCADE"), nullable=False)
    transaction_time = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())
    status = Column(String, nullable=False)

    last_updated = Column(TIMESTAMP(timezone=True), nullable=True, server_default=func.now())
