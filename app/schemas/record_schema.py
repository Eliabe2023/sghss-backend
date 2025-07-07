from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MedicalRecordBase(BaseModel):
    paciente_id: str
    profissional_id: str
    descricao: str
    data_registro: str

class MedicalRecordCreate(BaseModel):
    paciente_id: str
    profissional_id: str
    descricao: str
    data_registro: Optional[datetime] = None

class MedicalRecordUpdate(BaseModel):
    descricao: Optional[str] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
