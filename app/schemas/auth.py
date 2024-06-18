# app/schemas/auth.py

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Login(BaseModel):
    email: str
    password: str
