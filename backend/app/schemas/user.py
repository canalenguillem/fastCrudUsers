from pydantic import BaseModel
from typing import Optional
from app.schemas.profile import Profile  # Asegurarnos de importar el Profile


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    profile_id: Optional[int] = None


class User(UserBase):
    id: int
    is_active: bool
    # Cambiamos profile_id a profile para incluir la información completa del perfil
    profile: Optional[Profile]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    profile_id: Optional[int] = None
