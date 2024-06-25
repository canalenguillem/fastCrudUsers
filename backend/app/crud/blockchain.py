from sqlalchemy.orm import Session
from app.models.blockchain import Blockchain as BlockchainModel
from app.models.blockchain import Blockchain

from app.schemas.blockchain import BlockchainCreate as BlockchainCreateSchema


def create_blockchain(db: Session, blockchain: BlockchainCreateSchema):
    db_blockchain = BlockchainModel(
        name=blockchain.name, node_url=blockchain.node_url)
    db.add(db_blockchain)
    db.commit()
    db.refresh(db_blockchain)
    return db_blockchain

def get_blockchain_by_id(db: Session, blockchain_id: int) -> Blockchain:
    return db.query(Blockchain).filter(Blockchain.id == blockchain_id).first()



def get_blockchain_by_name(db: Session, name: str):
    return db.query(BlockchainModel).filter(BlockchainModel.name == name).first()


def get_blockchains(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BlockchainModel).offset(skip).limit(limit).all()


def update_blockchain(db: Session, blockchain_id: int, blockchain: BlockchainCreateSchema):
    db_blockchain = db.query(BlockchainModel).filter(
        BlockchainModel.id == blockchain_id).first()
    if db_blockchain:
        db_blockchain.name = blockchain.name
        db_blockchain.node_url = blockchain.node_url
        db.commit()
        db.refresh(db_blockchain)
    return db_blockchain
