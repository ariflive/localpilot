import pytest
from app.services.ollama_inference import ollama_inference


@pytest.mark.asyncio
async def test_ollama_unavailable_graceful():
    # Should handle gracefully when Ollama not available
    result = await ollama_inference.generate("test")
    assert isinstance(result, dict)
    assert "success" in result
    # If unavailable, success should be False
    if not result.get("success"):
        assert "error" in result
