from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.portfolio import create_portfolio, get_portfolio, get_portfolios_by_user_id, add_address_to_portfolio,get_addresses_by_portfolio_id
from app.schemas.portfolio import PortfolioCreate, PortfolioOut
from app.schemas.address import AddressCreate, AddressOut
from app.db.database import get_db
from app.routers.auth import get_current_active_user
from app.models.user import User
from app.crud.erc20_token import get_tokens_by_blockchain_id
from app.ethereum import get_token_balance


router = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
)

@router.post("/", response_model=PortfolioOut)
def create_new_portfolio(portfolio: PortfolioCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_portfolio(db=db, portfolio=portfolio, user_id=current_user.id)

@router.get("/{portfolio_id}", response_model=PortfolioOut)
def read_portfolio(portfolio_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_portfolio = get_portfolio(db, portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_portfolio

@router.get("/user/{user_id}", response_model=List[PortfolioOut])
def read_user_portfolios(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_portfolios_by_user_id(db, user_id)

@router.post("/{portfolio_id}/address", response_model=AddressOut)
def add_address(portfolio_id: int, address: AddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return add_address_to_portfolio(db, address, portfolio_id)

@router.get("/{portfolio_id}/balances/{blockchain_id}")
def get_portfolio_balances(portfolio_id: int, blockchain_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    addresses = get_addresses_by_portfolio_id(db, portfolio_id)
    if not addresses:
        raise HTTPException(status_code=404, detail="Portfolio not found or no addresses associated with the portfolio")

    tokens = get_tokens_by_blockchain_id(db, blockchain_id)
    if not tokens:
        raise HTTPException(status_code=404, detail="No tokens found for the specified blockchain")

    balances: Dict[str, Dict[str, float]] = {}
    for address in addresses:
        address_balances = {}
        for token in tokens:
            token_balance = get_token_balance(db, address.address, token.id)
            address_balances[token.symbol] = token_balance["balance"]
        balances[address.address] = address_balances

    return balances
