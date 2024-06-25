from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.erc20_token import Token
from app.crud.erc20_token import get_tokens_by_blockchain_id, create_token
from app.db.database import get_db
from app.routers.auth import get_current_admin_user
from app.schemas.erc20_token import TokenCreate

router = APIRouter()

@router.post("/", response_model=Token, dependencies=[Depends(get_current_admin_user)])
def create_erc20_token(token: TokenCreate, db: Session = Depends(get_db)):
    db_token = create_token(db, token)
    if not db_token:
        raise HTTPException(status_code=400, detail="Token could not be created")
    return db_token

@router.get("/by_blockchain/{blockchain_id}", response_model=list[Token])
def get_erc20_tokens_by_blockchain(blockchain_id: int, db: Session = Depends(get_db)):
    tokens = get_tokens_by_blockchain_id(db, blockchain_id)
    if not tokens:
        raise HTTPException(status_code=404, detail="No tokens found for this blockchain")
    return tokens
