from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Blockchain(Base):
    __tablename__ = "blockchains"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    node_url = Column(String, nullable=False)
    
    tokens = relationship("ERC20Token", back_populates="blockchain")
