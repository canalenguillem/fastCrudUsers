from pydantic import BaseModel


class BlockchainBase(BaseModel):
    name: str
    node_url: str


class BlockchainCreate(BlockchainBase):
    pass


class Blockchain(BlockchainBase):
    id: int

    class Config:
        from_attributes = True
