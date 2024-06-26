from pydantic import BaseModel

class DEXBase(BaseModel):
    name: str
    factory_address: str
    router_address: str
    blockchain_id: int
    factory_abi_path: str
    router_abi_path: str

class DEXCreate(DEXBase):
    pass

class DEXUpdate(DEXBase):
    pass

class DEX(DEXBase):
    id: int

    class Config:
        from_attributes = True
