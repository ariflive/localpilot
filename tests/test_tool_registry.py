import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_tool_registry_allowlist():
    from app.services.tool_registry import tool_registry
    tools = tool_registry.list_tools()
    assert len(tools) > 0
    # shell/python exec must not be in allowlist
    names = [t["name"] for t in tools]
    assert "shell" not in names
    assert "exec" not in names
    assert "eval" not in names
    assert "run_python" not in names
