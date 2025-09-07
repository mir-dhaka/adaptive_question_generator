import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_read_items_integration():
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.get("/items")
        assert res.status_code == 200
        assert "message" in res.json()
