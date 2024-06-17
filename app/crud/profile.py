# app/crud/profile.py

from sqlalchemy.orm import Session
from app.models import profile as models
# Importar el modelo de usuario para la verificación
from app.models.user import User
from app.schemas import profile as schemas


def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(name=profile.name)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_profiles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Profile).offset(skip).limit(limit).all()


def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()


def delete_profile(db: Session, profile_id: int):
    db_profile = db.query(models.Profile).filter(
        models.Profile.id == profile_id).first()
    if db_profile:
        # Verificar si existen usuarios asociados a este perfil
        users_with_profile = db.query(User).filter(
            User.profile_id == profile_id).count()
        if users_with_profile > 0:
            raise ValueError("Cannot delete profile with associated users")
        db.delete(db_profile)
        db.commit()
    return db_profile
