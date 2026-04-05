from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    type = Column(String)
    category = Column(String)
    date = Column(Date)
    notes = Column(String)
    is_deleted = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))    
    user = relationship("User", back_populates="records")