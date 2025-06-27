from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentCreate(BaseModel):
    paciente_id: str
    profissional_id: str
    data_hora: datetime
    motivo: Optional[str] = None

class AppointmentUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    motivo: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: str
    paciente_id: str
    profissional_id: str
    data_hora: datetime
    motivo: Optional[str] = None
