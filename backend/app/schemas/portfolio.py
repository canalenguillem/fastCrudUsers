from pydantic import BaseModel
from typing import List
from app.schemas.address import AddressOut

class PortfolioBase(BaseModel):
    name: str
    user_id: int

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(PortfolioBase):
    pass

class PortfolioOut(PortfolioBase):
    id: int
    addresses: List[AddressOut]

    class Config:
        from_attributes = True
