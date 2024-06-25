from pydantic import BaseModel

class TokenBase(BaseModel):
    name: str
    symbol: str
    contract_address: str
    blockchain_id: int

class TokenCreate(TokenBase):
    pass

class TokenUpdate(TokenBase):
    pass

class Token(TokenBase):
    id: int

    class Config:
        from_attributes = True
