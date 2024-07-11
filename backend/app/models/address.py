from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.portfolio import portfolio_address_association

class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True, nullable=False, unique=True)
    
    portfolios = relationship('Portfolio', secondary=portfolio_address_association, back_populates='addresses')
