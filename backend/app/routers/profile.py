# app/routers/profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import profile as crud
from app.schemas import profile as schemas
from app.db.database import get_db
from app.routers.auth import get_current_admin_user

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"]
)


@router.post("/profiles/", response_model=schemas.Profile)
def create_profile(
    profile: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan crear perfiles
    current_user=Depends(get_current_admin_user)
):
    return crud.create_profile(db=db, profile=profile)


@router.get("/profiles/", response_model=List[schemas.Profile])
def read_profiles(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan leer todos los perfiles
    current_user=Depends(get_current_admin_user)
):
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles


@router.get("/profiles/{profile_id}", response_model=schemas.Profile)
def read_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan leer un perfil por ID
    current_user=Depends(get_current_admin_user)
):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.delete("/profiles/{profile_id}", response_model=schemas.Profile)
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    # Asegura que solo los administradores puedan eliminar perfiles
    current_user=Depends(get_current_admin_user)
):
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    try:
        return crud.delete_profile(db=db, profile_id=profile_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
