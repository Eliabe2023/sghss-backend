import pytest

@pytest.mark.asyncio
async def test_pacientes_crud(client):
    paciente_data = {
        "nome": "Teste Paciente",
        "cpf": "12345678900",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "endereco": "Rua Teste, 123"
    }
    response = await client.post("/patients/", json=paciente_data)
    print("CREATE:", response.status_code, response.json())
    assert response.status_code == 200
    paciente = response.json()
    assert paciente["nome"] == paciente_data["nome"]
    assert paciente["cpf"] == paciente_data["cpf"]

    # Excluir o paciente criado
    response = await client.delete(f"/patients/{paciente['id']}")
    print("DELETE:", response.status_code, response.json())
    assert response.status_code == 200
