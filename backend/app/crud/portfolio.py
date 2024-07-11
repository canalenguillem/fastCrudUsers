from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.address import Address
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.schemas.address import AddressCreate

def create_portfolio(db: Session, portfolio: PortfolioCreate, user_id: int) -> Portfolio:
    db_portfolio = Portfolio(name=portfolio.name, user_id=user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def get_portfolio(db: Session, portfolio_id: int) -> Portfolio:
    return db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

def get_portfolios_by_user_id(db: Session, user_id: int):
    return db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

def add_address_to_portfolio(db: Session, address: AddressCreate, portfolio_id: int) -> Address:
    db_address = db.query(Address).filter(Address.address == address.address).first()
    if db_address is None:
        db_address = Address(address=address.address)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
    db_portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if db_portfolio:
        db_portfolio.addresses.append(db_address)
        db.commit()
        db.refresh(db_portfolio)
    return db_address
