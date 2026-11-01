import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_duplicate_task():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"title": "Test", "description": "Test task"}
        r1 = await ac.post("/api/v1/tasks", json=payload)
        assert r1.status_code == 200
        r2 = await ac.post("/api/v1/tasks", json=payload)
        assert r2.status_code == 200
        assert r1.json()["id"] != r2.json()["id"]
