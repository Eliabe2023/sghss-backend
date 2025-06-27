from fastapi import APIRouter, HTTPException
from uuid import uuid4
from datetime import datetime
from app.services.firebase import db

from app.schemas.record_schema import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse

router = APIRouter()
records_collection = db.collection("medical_records")

@router.post("/records/", response_model=MedicalRecordResponse)
def create_record(record: MedicalRecordCreate):
    record_id = str(uuid4())
    data = {
        "id": record_id,
        "paciente_id": record.paciente_id,
        "profissional_id": record.profissional_id,
        "descricao": record.descricao,
        "data_registro": (record.data_registro or datetime.now()).isoformat()
    }
    records_collection.document(record_id).set(data)
    return MedicalRecordResponse(**data)

@router.get("/records/", response_model=list[MedicalRecordResponse])
def list_records():
    docs = records_collection.stream()
    return [MedicalRecordResponse(**{**doc.to_dict(), "data_registro": doc.to_dict()["data_registro"]}) for doc in docs]

@router.put("/records/{record_id}", response_model=MedicalRecordResponse)
def update_record(record_id: str, update: MedicalRecordUpdate):
    ref = records_collection.document(record_id)
    doc = ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado.")

    update_data = {}
    if update.descricao:
        update_data["descricao"] = update.descricao

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhuma atualização enviada.")

    ref.update(update_data)
    updated = ref.get().to_dict()
    return MedicalRecordResponse(**updated)

@router.delete("/records/{record_id}")
def delete_record(record_id: str):
    ref = records_collection.document(record_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Prontuário não encontrado.")
    ref.delete()
    return {"message": "Prontuário excluído com sucesso."}
