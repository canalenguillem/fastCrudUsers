from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.erc20_token import TokenCreate, Token
from app.crud.erc20_token import create_token
from app.db.database import get_db
from app.routers.auth import get_current_admin_user

router = APIRouter()

@router.post("/erc20_tokens/", response_model=Token, dependencies=[Depends(get_current_admin_user)])
def create_erc20_token(token: TokenCreate, db: Session = Depends(get_db)):
    db_token = create_token(db, token)
    if not db_token:
        raise HTTPException(status_code=400, detail="Token could not be created")
    return db_token
