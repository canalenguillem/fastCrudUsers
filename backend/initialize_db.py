from sqlalchemy.orm import Session
from app.db.database import Base, engine
from app.models import user as user_models, profile as profile_models, blockchain as blockchain_models
from app.crud import user as crud_user, profile as crud_profile, blockchain as crud_blockchain
from app.schemas import user as schemas_user, profile as schemas_profile, blockchain as schemas_blockchain
from decouple import config

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

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
    password="adminpass",
    profile_id=admin_profile.id
)
default_user = schemas_user.UserCreate(
    username="user",
    email="user@example.com",
    password="userpass",
    profile_id=user_profile.id
)

crud_user.create_user(db=db, user=admin_user)
crud_user.create_user(db=db, user=default_user)

# Añadir información de redes blockchain
blockchains = [
    schemas_blockchain.BlockchainCreate(
        name="ethereum", node_url=config("ETHEREUM_NODE_URL")),
    schemas_blockchain.BlockchainCreate(
        name="pulsechain", node_url="https://rpc.pulsechain.com"),
    schemas_blockchain.BlockchainCreate(
        name="base", node_url="https://mainnet.base.org")
]

for blockchain in blockchains:
    crud_blockchain.create_blockchain(db, blockchain)

db.commit()
db.close()

print("Base de datos inicializada con perfiles, usuarios y blockchains predeterminados.")
