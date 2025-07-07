from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    endereco: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[date] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class PatientResponse(PatientBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
