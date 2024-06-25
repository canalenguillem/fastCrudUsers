from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class ERC20Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    symbol = Column(String, index=True)
    contract_address = Column(String, unique=True, index=True)
    blockchain_id = Column(Integer, ForeignKey('blockchains.id'))

    blockchain = relationship("Blockchain", back_populates="tokens")
