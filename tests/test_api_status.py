import pytest

@pytest.mark.asyncio
async def test_api_status(client):
    response = await client.get("/api/status")
    assert response.status_code == 200
    # Ajuste conforme o que sua API realmente retorna:
    assert response.json() == {"message": "A API está rodando"}
