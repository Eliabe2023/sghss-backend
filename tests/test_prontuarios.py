import pytest
import uuid

@pytest.mark.asyncio
async def test_prontuarios_crud(client):
    cpf_unico = str(uuid.uuid4().int)[:11]

    paciente_data = {
        "nome": "Prontuario Paciente",
        "cpf": cpf_unico,
        "data_nascimento": "1985-07-20",
        "telefone": "11999991111",
        "endereco": "Rua Prontuario, 456"
    }
    r_paciente = await client.post("/patients/", json=paciente_data)
    assert r_paciente.status_code == 200, f"Erro ao criar paciente: {r_paciente.text}"
    paciente = r_paciente.json()

    crm_unico = f"CRM{uuid.uuid4().hex[:6]}"
    prof_data = {
        "nome": "Prontuario Prof",
        "especialidade": "Dermatologia",
        "crm": crm_unico,
        "telefone": "11988886666",
        "email": f"prontuario{uuid.uuid4().hex[:6]}@prof.com"
    }
    r_prof = await client.post("/professionals/", json=prof_data)
    assert r_prof.status_code == 200, f"Erro ao criar profissional: {r_prof.text}"
    profissional = r_prof.json()

    prontuario_data = {
        "paciente_id": paciente["id"],
        "profissional_id": profissional["id"],
        "descricao": "Consulta inicial"
    }
    r_pront = await client.post("/records/", json=prontuario_data)
    assert r_pront.status_code == 200, f"Erro ao criar prontuário: {r_pront.text}"
    prontuario = r_pront.json()

    # Update
    update_data = {"descricao": "Revisão"}
    r_update = await client.put(f"/records/{prontuario['id']}", json=update_data)
    assert r_update.status_code == 200, f"Erro ao atualizar prontuário: {r_update.text}"

    # Delete
    r_delete = await client.delete(f"/records/{prontuario['id']}")
    assert r_delete.status_code == 200, f"Erro ao excluir prontuário: {r_delete.text}"
