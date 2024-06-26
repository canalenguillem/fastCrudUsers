from sqlalchemy.orm import Session
from app.db.database import Base, engine
from app.models import user as user_models, profile as profile_models, blockchain as blockchain_models, dex as dex_models, erc20_token as erc20_token_models
from app.crud import user as crud_user, profile as crud_profile, blockchain as crud_blockchain, dex as crud_dex
from app.schemas import user as schemas_user, profile as schemas_profile, blockchain as schemas_blockchain, dex as schemas_dex
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

# Añadir DEX predeterminado
pulsexv2_dex = schemas_dex.DEXCreate(
    name="PULSEXv2",
    factory_address="0x29eA7545DEf87022BAdc76323F373EA1e707C523",
    router_address="0x165C3410fC91EF562C50559f7d2289fEbed552d9",
    blockchain_id=2,  # Asumimos que el ID de PulseChain es 2
    factory_abi_path="abis/pulsexv2_factory.py",
    router_abi_path="abis/pulsexv2_router.py"
)

crud_dex.create_dex(db, pulsexv2_dex)

db.commit()
db.close()

print("Base de datos inicializada con perfiles, usuarios, blockchains y DEX predeterminados.")
