import pytest

@pytest.mark.asyncio
async def test_profissionais_crud(client):
    prof_data = {
        "nome": "Prof Teste",
        "especialidade": "Ortopedia",
        "crm": "CRM98765",
        "telefone": "11988888888",
        "email": "prof@teste.com"
    }
    response = await client.post("/professionals/", json=prof_data)
    print("CREATE:", response.status_code, response.json())
    assert response.status_code == 200
    profissional = response.json()
    assert profissional["nome"] == prof_data["nome"]
    assert profissional["crm"] == prof_data["crm"]

    # Excluir o profissional criado
    response = await client.delete(f"/professionals/{profissional['id']}")
    print("DELETE:", response.status_code, response.json())
    assert response.status_code == 200
