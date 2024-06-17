# app/schemas/profile.py

from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str


class ProfileCreate(ProfileBase):
    pass


class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True
