from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.schemas import user as schemas_user
from app.schemas.user import User as UserSchema

from app.db.database import get_db
from typing import List
from app.routers.auth import get_current_admin_user, get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=schemas_user.User, dependencies=[Depends(get_current_admin_user)])
def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas_user.User], dependencies=[Depends(get_current_admin_user)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/me", response_model=UserSchema)
def read_users_me(current_user: UserSchema = Depends(get_current_active_user),
                  db: Session = Depends(get_db)):
    print("in readuserme")
    return current_user


@router.put("/{user_id}", response_model=schemas_user.User, dependencies=[Depends(get_current_admin_user)])
def update_user(user_id: int, user: schemas_user.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db=db, db_user=db_user, user_update=user)
