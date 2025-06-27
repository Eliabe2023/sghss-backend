from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True
