from fastapi import APIRouter, HTTPException
from uuid import uuid4
from app.schemas.professional_schema import ProfessionalCreate, ProfessionalUpdate, ProfessionalResponse
from app.services.firebase import db

router = APIRouter()
professionals_collection = db.collection("professionals")

@router.post("/professionals/", response_model=ProfessionalResponse)
def create_professional(prof: ProfessionalCreate):
    existing = professionals_collection.where("crm", "==", prof.crm).stream()
    if any(existing):
        raise HTTPException(status_code=400, detail="CRM já cadastrado.")

    prof_id = str(uuid4())
    data = {
        "id": prof_id,
        "nome": prof.nome,
        "especialidade": prof.especialidade,
        "crm": prof.crm,
        "telefone": prof.telefone,
        "email": prof.email
    }

    professionals_collection.document(prof_id).set(data)
    return ProfessionalResponse(**data)

@router.get("/professionals/", response_model=list[ProfessionalResponse])
def list_professionals():
    docs = professionals_collection.stream()
    return [ProfessionalResponse(**doc.to_dict()) for doc in docs]

@router.put("/professionals/{prof_id}", response_model=ProfessionalResponse)
def update_professional(prof_id: str, update: ProfessionalUpdate):
    ref = professionals_collection.document(prof_id)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")

    data = {}
    if update.nome: data["nome"] = update.nome
    if update.especialidade: data["especialidade"] = update.especialidade
    if update.telefone: data["telefone"] = update.telefone
    if update.email: data["email"] = update.email

    if not data:
        raise HTTPException(status_code=400, detail="Nenhuma informação enviada para atualização.")

    ref.update(data)
    updated_doc = ref.get().to_dict()
    return ProfessionalResponse(**updated_doc)

@router.delete("/professionals/{prof_id}")
def delete_professional(prof_id: str):
    ref = professionals_collection.document(prof_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")

    ref.delete()
    return {"message": "Profissional excluído com sucesso."}
