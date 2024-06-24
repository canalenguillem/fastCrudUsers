from fastapi import APIRouter, HTTPException
from app.ethereum import get_balance

router = APIRouter(
    prefix="/ethereum",
    tags=["ethereum"]
)


@router.get("/balance/{address}")
def read_balance(address: str):
    try:
        balance = get_balance(address)
        return {"address": address, "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
