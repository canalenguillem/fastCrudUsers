from pydantic import BaseModel

class AddressBase(BaseModel):
    address: str

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class AddressOut(AddressBase):
    id: int

    class Config:
        from_attributes = True
