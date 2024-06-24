# app/routers/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import user as crud_user
from app.crud import profile as crud_profile
from app.schemas import user as schemas_user
from app.db.database import get_db
from app.models.user import User  # Importa el modelo User
from app.routers.auth import get_current_admin_user

router = APIRouter()


@router.post("/users/", response_model=schemas_user.User)
def create_user(
    user: schemas_user.UserCreate,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan crear usuarios
    current_user: User = Depends(get_current_admin_user)
):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_profile = crud_profile.get_profile(db, profile_id=user.profile_id)
    if db_profile is None:
        raise HTTPException(status_code=400, detail="Profile does not exist")

    user_created = crud_user.create_user(db=db, user=user)
    print(f"usuario creado: {user_created}")  # Agregar print para depuración
    return user_created


@router.get("/users/", response_model=List[schemas_user.User])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan leer todos los usuarios
    current_user: User = Depends(get_current_admin_user)
):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas_user.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan leer un usuario por ID
    current_user: User = Depends(get_current_admin_user)
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}", response_model=schemas_user.User)
def update_user(
    user_id: int,
    user: schemas_user.UserUpdate,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan actualizar usuarios
    current_user: User = Depends(get_current_admin_user)
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db=db, user_id=user_id, user_update=user)


@router.delete("/users/{user_id}", response_model=schemas_user.User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan borrar usuarios
    current_user: User = Depends(get_current_admin_user)
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.delete_user(db=db, user_id=user_id)


@router.put("/users/{user_id}/assign-profile/{profile_id}", response_model=schemas_user.User)
def assign_profile_to_user(
    user_id: int,
    profile_id: int,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan asignar perfiles
    current_user: User = Depends(get_current_admin_user)
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_profile = crud_profile.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return crud_user.assign_profile_to_user(db=db, user_id=user_id, profile_id=profile_id)
