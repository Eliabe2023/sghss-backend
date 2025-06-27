from fastapi import APIRouter, HTTPException
from uuid import uuid4
from app.schemas.patient_schema import PatientCreate, PatientUpdate, PatientResponse
from app.services.firebase import db  # Corrigido o caminho para a pasta correta

router = APIRouter()
patients_collection = db.collection("patients")

@router.post("/patients/", response_model=PatientResponse)
def create_patient(patient: PatientCreate):
    existing = patients_collection.where("cpf", "==", patient.cpf).stream()
    if any(existing):
        raise HTTPException(status_code=400, detail="Paciente com este CPF já existe.")

    patient_id = str(uuid4())
    patient_data = {
        "id": patient_id,
        "nome": patient.nome,
        "cpf": patient.cpf,
        "data_nascimento": patient.data_nascimento.isoformat(),
        "telefone": patient.telefone,
        "endereco": patient.endereco
    }

    patients_collection.document(patient_id).set(patient_data)
    return PatientResponse(**patient_data)

@router.get("/patients/", response_model=list[PatientResponse])
def list_patients():
    docs = patients_collection.stream()
    return [PatientResponse(**doc.to_dict()) for doc in docs]

@router.put("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: str, update: PatientUpdate):
    patient_ref = patients_collection.document(patient_id)
    doc = patient_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    update_data = {}

    if update.nome is not None:
        update_data["nome"] = update.nome
    if update.telefone is not None:
        update_data["telefone"] = update.telefone
    if update.endereco is not None:
        update_data["endereco"] = update.endereco

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhuma informação para atualizar.")

    patient_ref.update(update_data)
    return PatientResponse(**patient_ref.get().to_dict())

@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    patient_ref = patients_collection.document(patient_id)
    doc = patient_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    patient_ref.delete()
    return {"message": "Paciente deletado com sucesso."}
