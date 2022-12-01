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
