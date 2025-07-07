import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def novo_paciente(client):
    paciente_data = {"nome": "Paciente Teste", "idade": 30, "cpf": "11122233344"}
    response = await client.post("/pacientes/novo", json=paciente_data)
    paciente = response.json()
    yield paciente
    await client.delete(f"/pacientes/excluir/{paciente['id']}")

@pytest_asyncio.fixture
async def novo_profissional(client):
    profissional_data = {"nome": "Prof Teste", "especialidade": "Ortopedia", "crm": "CRM54321"}
    response = await client.post("/profissionais/novo", json=profissional_data)
    profissional = response.json()
    yield profissional
    await client.delete(f"/profissionais/excluir/{profissional['id']}")
