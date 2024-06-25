from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.blockchain import create_blockchain, get_blockchains, get_blockchain_by_name, update_blockchain
from app.schemas.blockchain import BlockchainCreate, Blockchain
from app.db.database import get_db
from typing import List
from app.routers.auth import get_current_admin_user

router = APIRouter(
    prefix="/blockchains",
    tags=["blockchains"]
)


@router.post("/", response_model=Blockchain, dependencies=[Depends(get_current_admin_user)])
def create_new_blockchain(blockchain: BlockchainCreate, db: Session = Depends(get_db)):
    db_blockchain = get_blockchain_by_name(db, name=blockchain.name)
    if db_blockchain:
        raise HTTPException(
            status_code=400, detail="Blockchain already registered")
    return create_blockchain(db=db, blockchain=blockchain)


@router.get("/", response_model=List[Blockchain])
def read_blockchains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blockchains = get_blockchains(db, skip=skip, limit=limit)
    return blockchains


@router.put("/{blockchain_id}", response_model=Blockchain, dependencies=[Depends(get_current_admin_user)])
def update_existing_blockchain(blockchain_id: int, blockchain: BlockchainCreate, db: Session = Depends(get_db)):
    db_blockchain = update_blockchain(
        db=db, blockchain_id=blockchain_id, blockchain=blockchain)
    if db_blockchain is None:
        raise HTTPException(status_code=404, detail="Blockchain not found")
    return db_blockchain
