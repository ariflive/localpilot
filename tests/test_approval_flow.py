import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_approval_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create approval request
        r = await ac.post("/api/v1/approvals", json={"tool_name": "web_search", "tool_args": {"query": "test"}})
        assert r.status_code == 200
        data = r.json()
        assert "approval_id" in data
        approval_id = data["approval_id"]
        # Approve
        r2 = await ac.post(f"/api/v1/approvals/{approval_id}/respond", json={"action": "approve"})
        assert r2.status_code == 200
        # Reject another
        r3 = await ac.post("/api/v1/approvals", json={"tool_name": "web_search", "tool_args": {"query": "test2"}})
        approval_id2 = r3.json()["approval_id"]
        r4 = await ac.post(f"/api/v1/approvals/{approval_id2}/respond", json={"action": "reject"})
        assert r4.status_code == 200
