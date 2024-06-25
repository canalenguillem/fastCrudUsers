from fastapi import APIRouter, HTTPException, Depends
from app.ethereum import get_balance
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/ethereum",
    tags=["ethereum"]
)


@router.get("/balance/{blockchain_name}/{address}")
def read_balance(blockchain_name: str, address: str, db: Session = Depends(get_db)):
    try:
        balance = get_balance(db, blockchain_name, address)
        return {"blockchain": blockchain_name, "address": address, "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
