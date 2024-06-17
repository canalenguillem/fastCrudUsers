# app/schemas/user.py

from pydantic import BaseModel
from typing import Optional
from app.schemas.profile import Profile


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    profile_id: int


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    profile_id: Optional[int] = None


class User(UserBase):
    id: int
    profile: Profile

    class Config:
        orm_mode = True
