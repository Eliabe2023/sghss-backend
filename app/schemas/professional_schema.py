from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProfessionalBase(BaseModel):
    nome: str
    especialidade: str
    crm: str
    telefone: str
    email: str

class ProfessionalCreate(ProfessionalBase):
    pass

class ProfessionalUpdate(BaseModel):
    nome: Optional[str] = None
    especialidade: Optional[str] = None
    crm: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None

class ProfessionalResponse(ProfessionalBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
