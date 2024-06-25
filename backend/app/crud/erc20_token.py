from sqlalchemy.orm import Session
from app.models.erc20_token import ERC20Token
from app.schemas.erc20_token import TokenCreate, TokenUpdate

def get_token_by_id(db: Session, token_id: int) -> ERC20Token:
    return db.query(ERC20Token).filter(ERC20Token.id == token_id).first()

def get_tokens_by_blockchain_id(db: Session, blockchain_id: int):
    return db.query(ERC20Token).filter(ERC20Token.blockchain_id == blockchain_id).all()

def create_token(db: Session, token: TokenCreate) -> ERC20Token:
    db_token = ERC20Token(
        name=token.name, 
        symbol=token.symbol, 
        contract_address=token.contract_address, 
        blockchain_id=token.blockchain_id
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def update_token(db: Session, token_id: int, token_update: TokenUpdate) -> ERC20Token:
    db_token = get_token_by_id(db, token_id)
    if db_token:
        db_token.name = token_update.name
        db_token.symbol = token_update.symbol
        db_token.contract_address = token_update.contract_address
        db_token.blockchain_id = token_update.blockchain_id
        db.commit()
        db.refresh(db_token)
    return db_token

def delete_token(db: Session, token_id: int):
    db_token = get_token_by_id(db, token_id)
    if db_token:
        db.delete(db_token)
        db.commit()
