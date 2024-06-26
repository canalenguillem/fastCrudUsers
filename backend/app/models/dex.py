from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class DEX(Base):
    __tablename__ = 'dexes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    factory_address = Column(String, unique=True, index=True)
    router_address = Column(String, unique=True, index=True)
    blockchain_id = Column(Integer, ForeignKey('blockchains.id'))
    factory_abi_path = Column(String)
    router_abi_path = Column(String)

    blockchain = relationship("Blockchain", back_populates="dexes")
