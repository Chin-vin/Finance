from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    records = relationship("Record", back_populates="user")