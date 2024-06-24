from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)

    users = relationship("User", back_populates="profile")
