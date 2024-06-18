# app/crud/auth.py (un nuevo archivo para manejar autenticación)

import bcrypt
from sqlalchemy.orm import Session
from app.models import user as models


def authenticate_user(db: Session, email: str, password: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user and bcrypt.checkpw(password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        return db_user
    return None
