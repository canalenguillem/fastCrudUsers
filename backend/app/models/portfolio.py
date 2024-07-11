from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

portfolio_address_association = Table(
    'portfolio_address_association', Base.metadata,
    Column('portfolio_id', Integer, ForeignKey('portfolios.id')),
    Column('address_id', Integer, ForeignKey('addresses.id'))
)

class Portfolio(Base):
    __tablename__ = 'portfolios'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    addresses = relationship('Address', secondary=portfolio_address_association, back_populates='portfolios')
    user = relationship('User', back_populates='portfolios')
