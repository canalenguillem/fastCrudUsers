from sqlalchemy.orm import Session
from app.db.database import Base, engine
from app.models import user as user_models, profile as profile_models, blockchain as blockchain_models, dex as dex_models, erc20_token as erc20_token_models
from app.crud import user as crud_user, profile as crud_profile, blockchain as crud_blockchain, dex as crud_dex, erc20_token as crud_erc20_token
from app.schemas import user as schemas_user, profile as schemas_profile, blockchain as schemas_blockchain, dex as schemas_dex, erc20_token as schemas_erc20_token
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
    blockchain_id=2,  # ID de PulseChain
    factory_abi_path="abis/pulsexv2_factory.py",
    router_abi_path="abis/pulsexv2_router.py"
)

crud_dex.create_dex(db, pulsexv2_dex)

# Añadir tokens ERC20 predeterminados
erc20_tokens = [
    schemas_erc20_token.TokenCreate(
        name="eDAI",
        symbol="eDAI",
        contract_address="0xefD766cCb38EaF1dfd701853BFCe31359239F305",
        blockchain_id=2  # ID de PulseChain
    ),
    schemas_erc20_token.TokenCreate(
        name="PLSX",
        symbol="PLSX",
        contract_address="0x95B303987A60C71504D99Aa1b13B4DA07b0790ab",
        blockchain_id=2  # ID de PulseChain
    ),
    schemas_erc20_token.TokenCreate(
        name="INC",
        symbol="INC",
        contract_address="0x2fa878Ab3F87CC1C9737Fc071108F904c0B0C95d",
        blockchain_id=2  # ID de PulseChain
    )
]

for token in erc20_tokens:
    crud_erc20_token.create_token(db, token)

db.commit()
db.close()

print("Base de datos inicializada con perfiles, usuarios, blockchains, DEX y tokens ERC20 predeterminados.")
