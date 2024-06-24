from sqlalchemy.orm import Session
from app.models import user as models
from app.schemas import user as schemas
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.models import profile as profile_models
from decouple import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = config("SECRET_KEY")
DEFAULT_PROFILE = config("DEFAULT_PROFILE")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    profile_id = user.profile_id
    if not profile_id:
        default_profile = db.query(profile_models.Profile).filter(
            profile_models.Profile.name == DEFAULT_PROFILE).first()
        if not default_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Default profile not found")
        profile_id = default_profile.id
    db_user = models.User(email=user.email, hashed_password=hashed_password,
                          username=user.username, profile_id=profile_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    update_data = user_update.dict(exclude_unset=True)
    if 'password' in update_data:
        update_data['hashed_password'] = get_password_hash(
            update_data.pop('password'))
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
