from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AppointmentBase(BaseModel):
    paciente_id: str
    profissional_id: str
    data_hora: datetime
    motivo: str

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    motivo: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
