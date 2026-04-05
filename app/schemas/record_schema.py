from pydantic import BaseModel, Field
from datetime import date

class RecordCreate(BaseModel):
    amount: float = Field(gt=0)
    type: str = Field(pattern="^(income|expense)$")
    category: str
    date: date
    notes: str

class RecordOut(RecordCreate):
    id: int

    class Config:
        from_attributes = True
        
        
