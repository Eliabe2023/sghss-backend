import pytest
import uuid

@pytest.mark.asyncio
async def test_users_crud(client):
    email_unico = f"user{uuid.uuid4().hex[:6]}@teste.com"
    user_data = {
        "nome": "User Teste",
        "email": email_unico,
        "senha": "senha123"
    }

    # Criar usuário
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 200, f"Falha ao criar usuário: {response.text}"
    user = response.json()
    assert user["nome"] == user_data["nome"]
    assert user["email"] == user_data["email"]

    # Atualizar usuário
    update_data = {
        "nome": "User Teste Atualizado",
        "email": f"updated{email_unico}",
        "senha": "novaSenha123"
    }
    response = await client.put(f"/users/{user['id']}", json=update_data)
    assert response.status_code == 200, f"Falha ao atualizar usuário: {response.text}"
    updated_user = response.json()
    assert updated_user["nome"] == update_data["nome"]
    assert updated_user["email"] == update_data["email"]

    # Listar usuários (só para confirmar que não dá erro)
    response = await client.get("/users/")
    assert response.status_code == 200, f"Falha ao listar usuários: {response.text}"
    users = response.json()
    assert any(u["id"] == user["id"] for u in users), "Usuário criado não encontrado na listagem"

    # Deletar usuário
    response = await client.delete(f"/users/{user['id']}")
    assert response.status_code == 200, f"Falha ao deletar usuário: {response.text}"
