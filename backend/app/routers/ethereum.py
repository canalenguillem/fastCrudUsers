from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.ethereum import get_balance
router = APIRouter(
    prefix="/ethereum",
    tags=["ethereum"],
)

@router.get("/balance/{blockchain_id}/{address}")
def read_balance(blockchain_id: int, address: str, db: Session = Depends(get_db)):
    try:
        balance = get_balance(db, blockchain_id, address)
        return {"blockchain_id": blockchain_id, "address": address, "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
