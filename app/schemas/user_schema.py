from pydantic import BaseModel

from app.core.enums import RoleEnum

class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum
    

class UserLogin(BaseModel):
    username: str
    password: str