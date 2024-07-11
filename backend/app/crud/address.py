from sqlalchemy.orm import Session
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate

def create_address(db: Session, address: AddressCreate) -> Address:
    db_address = Address(address=address.address)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address(db: Session, address_id: int) -> Address:
    return db.query(Address).filter(Address.id == address_id).first()

def get_address_by_string(db: Session, address: str) -> Address:
    return db.query(Address).filter(Address.address == address).first()

def update_address(db: Session, address_id: int, address_update: AddressUpdate) -> Address:
    db_address = get_address(db, address_id)
    if db_address:
        db_address.address = address_update.address
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
