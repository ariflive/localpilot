import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_web_search_creates_pending_approval():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/api/v1/tasks", json={"title": "Search web", "description": "Search the web for latest Python 3.12 release"})
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "pending_approval"
        # Check approvals created
        r2 = await ac.get("/api/v1/approvals")
        approvals = r2.json()
        pending = [a for a in approvals if a["status"] == "pending"]
        assert len(pending) > 0
        assert pending[0]["tool_name"] == "web_search"
