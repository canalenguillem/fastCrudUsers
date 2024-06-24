from sqlalchemy.orm import Session
from app.db.database import Base, engine
from app.models import user as user_models, profile as profile_models
from app.crud import user as crud_user, profile as crud_profile
from app.schemas import user as schemas_user, profile as schemas_profile

# Eliminar las tablas existentes y crear nuevas tablas
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Crear una nueva sesión de base de datos
db = Session(bind=engine)

# Crear perfiles predeterminados
admin_profile = crud_profile.create_profile(
    db, schemas_profile.ProfileCreate(name="admin", description="Admin profile"))
user_profile = crud_profile.create_profile(
    db, schemas_profile.ProfileCreate(name="user", description="User profile"))

# Crear usuarios predeterminados
admin_user = schemas_user.UserCreate(
    username="admin",
    email="admin@example.com",
    password="adminpass",  # Cambia esto a una contraseña segura en producción
    profile_id=admin_profile.id
)
default_user = schemas_user.UserCreate(
    username="user",
    email="user@example.com",
    password="userpass",  # Cambia esto a una contraseña segura en producción
    profile_id=user_profile.id
)

# Guardar los usuarios en la base de datos
crud_user.create_user(db=db, user=admin_user)
crud_user.create_user(db=db, user=default_user)

# Confirmar las transacciones y cerrar la sesión
db.commit()
db.close()

print("Base de datos inicializada con perfiles y usuarios predeterminados.")
