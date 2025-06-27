from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, UserUpdate
from app.services.firebase import db
from uuid import uuid4
import bcrypt
from app.utils.hashing import hash_password

router = APIRouter()
users_collection = db.collection("users")


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    existing_users = users_collection.where("email", "==", user.email).stream()
    if any(existing_users):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    senha_hash = bcrypt.hashpw(user.senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user_id = str(uuid4())
    user_data = {
        "id": user_id,
        "nome": user.nome,
        "email": user.email,
        "senha": senha_hash
    }

    users_collection.document(user_id).set(user_data)
    return UserResponse(id=user_id, nome=user.nome, email=user.email)


@router.get("/users/", response_model=list[UserResponse])
def list_users():
    docs = users_collection.stream()
    users = []

    for doc in docs:
        data = doc.to_dict()
        users.append(UserResponse(
            id=data["id"],
            nome=data["nome"],
            email=data["email"]
        ))

    return users


@router.post("/login/")
def login(user: UserLogin):
    matching_users = users_collection.where("email", "==", user.email).stream()
    for doc in matching_users:
        data = doc.to_dict()
        if bcrypt.checkpw(user.senha.encode("utf-8"), data["senha"].encode("utf-8")):
            return {
                "message": "Login bem-sucedido",
                "user_id": data["id"],
                "nome": data["nome"]
            }
        else:
            raise HTTPException(status_code=401, detail="Senha incorreta")

    raise HTTPException(status_code=404, detail="Usuário não encontrado")


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_update: UserUpdate):
    user_ref = users_collection.document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    update_data = {}

    if user_update.nome:
        update_data["nome"] = user_update.nome
    if user_update.email:
        update_data["email"] = user_update.email
    if user_update.senha:
        update_data["senha"] = hash_password(user_update.senha)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado enviado para atualização.")

    user_ref.update(update_data)

    updated_user = user_ref.get().to_dict()
    return UserResponse(
        id=updated_user["id"],
        nome=updated_user["nome"],
        email=updated_user["email"]
    )


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    user_ref = users_collection.document(user_id)
    if not user_ref.get().exists:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    user_ref.delete()
    return {"message": f"Usuário com ID {user_id} deletado com sucesso."}
