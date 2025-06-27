from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicalRecordCreate(BaseModel):
    paciente_id: str
    profissional_id: str
    descricao: str
    data_registro: Optional[datetime] = None  # Pode ser preenchida automaticamente

class MedicalRecordUpdate(BaseModel):
    descricao: Optional[str] = None

class MedicalRecordResponse(BaseModel):
    id: str
    paciente_id: str
    profissional_id: str
    descricao: str
    data_registro: datetime
