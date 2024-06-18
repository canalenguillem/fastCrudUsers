# app/initialize_db.py

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.profile import Profile
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.utils import get_password_hash


def init_db(db: Session):
    Base.metadata.create_all(bind=engine)

    admin_profile = Profile(name="admin")
    user_profile = Profile(name="user")

    db.add(admin_profile)
    db.add(user_profile)
    db.commit()
    db.refresh(admin_profile)
    db.refresh(user_profile)

    admin_user = UserCreate(username="guillem", email="guillem@example.com",
                            password="adminpassword", profile_id=admin_profile.id)
    user_user = UserCreate(username="maria", email="maria@example.com",
                           password="userpassword", profile_id=user_profile.id)

    create_user(db=db, user=admin_user)
    create_user(db=db, user=user_user)


if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
    db.close()
