from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfessionalCreate(BaseModel):
    nome: str
    especialidade: str
    crm: str
    telefone: str
    email: EmailStr

class ProfessionalUpdate(BaseModel):
    nome: Optional[str] = None
    especialidade: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None

class ProfessionalResponse(BaseModel):
    id: str
    nome: str
    especialidade: str
    crm: str
    telefone: str
    email: EmailStr
