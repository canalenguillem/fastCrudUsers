# app/main.py
# uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import user, profile, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    # URL de tu frontend (Vite usa el puerto 5173 por defecto)
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, tags=["users"])
app.include_router(profile.router, tags=["profiles"])
app.include_router(auth.router, tags=["auth"])
