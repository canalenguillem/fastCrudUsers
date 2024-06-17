# app/main.py

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user, profile

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(profile.router, prefix="/api/v1", tags=["profiles"])
