import pytest
import uuid

@pytest.mark.asyncio
async def test_consultas_crud(client):
    cpf_unico = str(uuid.uuid4().int)[:11]

    paciente_data = {
        "nome": "Consulta Paciente",
        "cpf": cpf_unico,
        "data_nascimento": "1990-05-10",
        "telefone": "11999990000",
        "endereco": "Rua Consulta, 321"
    }
    r_paciente = await client.post("/patients/", json=paciente_data)
    assert r_paciente.status_code == 200, f"Erro ao criar paciente: {r_paciente.text}"
    paciente = r_paciente.json()

    crm_unico = f"CRM{uuid.uuid4().hex[:6]}"
    prof_data = {
        "nome": "Consulta Prof",
        "especialidade": "Cardiologia",
        "crm": crm_unico,
        "telefone": "11988887777",
        "email": f"consulta{uuid.uuid4().hex[:6]}@prof.com"
    }
    r_prof = await client.post("/professionals/", json=prof_data)
    assert r_prof.status_code == 200, f"Erro ao criar profissional: {r_prof.text}"
    profissional = r_prof.json()

    consulta_data = {
        "paciente_id": paciente["id"],
        "profissional_id": profissional["id"],
        "data_hora": "2025-07-07T10:00:00",
        "motivo": "Rotina"
    }
    r_consulta = await client.post("/appointments/", json=consulta_data)
    assert r_consulta.status_code == 200, f"Erro ao criar consulta: {r_consulta.text}"
    consulta = r_consulta.json()

    # Update
    update_data = {"motivo": "Urgência"}
    r_update = await client.put(f"/appointments/{consulta['id']}", json=update_data)
    assert r_update.status_code == 200, f"Erro ao atualizar consulta: {r_update.text}"

    # Delete
    r_delete = await client.delete(f"/appointments/{consulta['id']}")
    assert r_delete.status_code == 200, f"Erro ao excluir consulta: {r_delete.text}"
