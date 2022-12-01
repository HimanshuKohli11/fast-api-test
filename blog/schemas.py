from typing import Optional, Union
from typing import List, Union
from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import datetime


# User
class UserCreate(BaseModel):
    """[summary]: Pydantic model for creating user
    """
    first_name: str
    last_name: str
    username: str
    password: str
    email: EmailStr
    mobile: int

    class Config:
        orm_mode = True


# class User(BaseModel):
#     name: str
#     email: str
#     password: str
#
#     class Config:
#         orm_mode = True


class ShowUser(BaseModel):
    first_name: str
    email: str

    class Config:
        orm_mode = True


# Profile
class UserProfile(BaseModel):
    """
    [summary]: User profile information for Profile page display at the app
    """

    team_name: str
    address: str
    name: str
    joined_at: datetime

    class Config:
        orm_mode = True


class ProfileUpdate(BaseModel):
    """
    [summary]: Pydantic model for creating as well as updating
    user profile
    """
    address: Union[str, None] = None
    team_name: Union[str, None] = None

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    """
    [summary]: used while creating the token
    """
    id: Optional[str] = None


class RefreshToken(BaseModel):
    id: int
    refresh_token: str


# Login
class Login(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class OTP(BaseModel):
    id: int
    otp: int


class Mobile(BaseModel):
    id: int
    mobile: str


class GameDetails(BaseModel):
    id: int
    date_of_play: str
    last_updated: str


class GameList(BaseModel):
    id: int
    date_of_play: datetime


class TeamCreate(BaseModel):
    team_name: str
    player_id_1: int
    player_id_2: int
    player_id_3: int
    player_id_4: int
    player_id_5: int
    player_id_6: int
    player_id_7: int
    player_id_8: int
    player_id_9: int
    player_id_10: int
    player_id_11: int
    player_id_12: int
    player_id_13: int


class TeamUpdate(BaseModel):
    player_id_1: Union[int, None] = None
    player_id_2: Union[int, None] = None
    player_id_3: Union[int, None] = None
    player_id_4: Union[int, None] = None
    player_id_5: Union[int, None] = None
    player_id_6: Union[int, None] = None
    player_id_7: Union[int, None] = None
    player_id_8: Union[int, None] = None
    player_id_9: Union[int, None] = None
    player_id_10: Union[int, None] = None
    player_id_11: Union[int, None] = None
    player_id_12: Union[int, None] = None
    player_id_13: Union[int, None] = None

