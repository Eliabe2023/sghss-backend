from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientCreate(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    endereco: str

class PatientUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class PatientResponse(BaseModel):
    id: str
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    endereco: str

    model_config = {
        "from_attributes": True
    }
