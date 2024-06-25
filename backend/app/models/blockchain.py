from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Blockchain(Base):
    __tablename__ = 'blockchains'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    node_url = Column(String)
