from fastapi import APIRouter, HTTPException
from uuid import uuid4
from app.services.firebase import db
from app.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate, AppointmentResponse

router = APIRouter()
appointments_collection = db.collection("appointments")

@router.post("/appointments/", response_model=AppointmentResponse)
def create_appointment(appt: AppointmentCreate):
    appt_id = str(uuid4())
    data = {
        "id": appt_id,
        "paciente_id": appt.paciente_id,
        "profissional_id": appt.profissional_id,
        "data_hora": appt.data_hora.isoformat(),
        "motivo": appt.motivo
    }
    appointments_collection.document(appt_id).set(data)
    return AppointmentResponse(**data)

@router.get("/appointments/", response_model=list[AppointmentResponse])
def list_appointments():
    docs = appointments_collection.stream()
    return [AppointmentResponse(**{**doc.to_dict(), "data_hora": doc.to_dict()["data_hora"]}) for doc in docs]

@router.put("/appointments/{appt_id}", response_model=AppointmentResponse)
def update_appointment(appt_id: str, update: AppointmentUpdate):
    ref = appointments_collection.document(appt_id)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")

    data = {}
    if update.data_hora:
        data["data_hora"] = update.data_hora.isoformat()
    if update.motivo:
        data["motivo"] = update.motivo

    if not data:
        raise HTTPException(status_code=400, detail="Nenhuma alteração enviada.")

    ref.update(data)
    updated = ref.get().to_dict()
    return AppointmentResponse(**updated)

@router.delete("/appointments/{appt_id}")
def delete_appointment(appt_id: str):
    ref = appointments_collection.document(appt_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    ref.delete()
    return {"message": "Consulta excluída com sucesso."}
