from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, profile, auth

app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:5173",  # Vite frontend
    # Agrega otros orígenes permitidos según sea necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(profile.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to fastCrud!"}
