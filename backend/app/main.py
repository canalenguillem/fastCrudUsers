from fastapi import FastAPI
from app.routers import user, profile, auth

app = FastAPI()

app.include_router(user.router)
app.include_router(profile.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to fastCrud!"}
