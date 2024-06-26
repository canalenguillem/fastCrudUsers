from sqlalchemy.orm import Session
from app.models.dex import DEX
from app.schemas.dex import DEXCreate, DEXUpdate

def get_dex_by_id(db: Session, dex_id: int) -> DEX:
    return db.query(DEX).filter(DEX.id == dex_id).first()

def get_dexes_by_blockchain_id(db: Session, blockchain_id: int):
    return db.query(DEX).filter(DEX.blockchain_id == blockchain_id).all()

def create_dex(db: Session, dex: DEXCreate) -> DEX:
    db_dex = DEX(
        name=dex.name,
        factory_address=dex.factory_address,
        router_address=dex.router_address,
        blockchain_id=dex.blockchain_id,
        factory_abi_path=dex.factory_abi_path,
        router_abi_path=dex.router_abi_path
    )
    db.add(db_dex)
    db.commit()
    db.refresh(db_dex)
    return db_dex

def update_dex(db: Session, dex_id: int, dex_update: DEXUpdate) -> DEX:
    db_dex = get_dex_by_id(db, dex_id)
    if db_dex:
        db_dex.name = dex_update.name
        db_dex.factory_address = dex_update.factory_address
        db_dex.router_address = dex_update.router_address
        db_dex.blockchain_id = dex_update.blockchain_id
        db_dex.factory_abi_path = dex_update.factory_abi_path
        db_dex.router_abi_path = dex_update.router_abi_path
        db.commit()
        db.refresh(db_dex)
    return db_dex

def delete_dex(db: Session, dex_id: int):
    db_dex = get_dex_by_id(db, dex_id)
    if db_dex:
        db.delete(db_dex)
        db.commit()
