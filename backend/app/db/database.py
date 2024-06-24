from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

# Leer las variables de entorno desde el archivo .env
DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia de base de datos


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
