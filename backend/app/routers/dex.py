from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.dex import DEX, DEXCreate
from app.crud import dex as crud_dex
from app.db.database import get_db
from app.routers.auth import get_current_admin_user
from app.ethereum import get_last_transactions, get_liquidity_amounts,get_token_price
from web3 import Web3

router = APIRouter(
    prefix="/dexes",
    tags=["dexes"]
)

@router.post("/", response_model=DEX, dependencies=[Depends(get_current_admin_user)])
def create_dex(dex: DEXCreate, db: Session = Depends(get_db)):
    db_dex = crud_dex.create_dex(db, dex)
    if not db_dex:
        raise HTTPException(status_code=400, detail="DEX could not be created")
    return db_dex

@router.get("/by_blockchain/{blockchain_id}", response_model=list[DEX])
def get_dexes_by_blockchain(blockchain_id: int, db: Session = Depends(get_db)):
    dexes = crud_dex.get_dexes_by_blockchain_id(db, blockchain_id)
    if not dexes:
        raise HTTPException(status_code=404, detail="No DEXes found for this blockchain")
    return dexes

@router.get("/{dex_id}/transactions", response_model=list)
def get_dex_transactions(dex_id: int, db: Session = Depends(get_db)):
    try:
        transactions = get_last_transactions(db, dex_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return [{
        "hash": tx.hash.hex(),
        "from": tx['from'],
        "to": tx.to,
        "value": Web3.fromWei(tx.value, 'ether'),
        "gas": tx.gas,
        "gasPrice": Web3.fromWei(tx.gasPrice, 'gwei')
    } for tx in transactions]

@router.get("/{dex_id}/liquidity", response_model=dict)
def get_dex_liquidity(dex_id: int, token0_address: str, token1_address: str, db: Session = Depends(get_db)):
    try:
        liquidity = get_liquidity_amounts(db, dex_id, token0_address, token1_address)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return liquidity

@router.get("/{dex_id}/price", response_model=float)
def get_dex_token_price(dex_id: int, token0_address: str, token1_address: str, db: Session = Depends(get_db)):
    try:
        price = get_token_price(db, dex_id, token0_address, token1_address)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return price
