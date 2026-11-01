import httpx
from loguru import logger
from typing import Dict, Any

from app.core.config import settings


class OllamaInferenceService:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model

    async def generate(self, prompt: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # Try /api/chat first (preferred)
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                }
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    content = data.get("message", {}).get("content", "") or data.get("response", "")
                    if not content:
                        return {"success": False, "error": "Empty response from model"}
                    return {"success": True, "response": content, "model": self.model}
                elif response.status_code == 404:
                    # Fallback to /api/generate
                    payload_gen = {"model": self.model, "prompt": prompt, "stream": False}
                    response2 = await client.post(f"{self.base_url}/api/generate", json=payload_gen)
                    if response2.status_code == 200:
                        data = response2.json()
                        content = data.get("response", "")
                        if not content:
                            return {"success": False, "error": "Empty response from model"}
                        return {"success": True, "response": content, "model": self.model}
                    return {"success": False, "error": f"Model not found or unavailable (status {response2.status_code})"}
                else:
                    return {"success": False, "error": f"Ollama error (status {response.status_code})"}
        except httpx.ConnectError:
            logger.warning("Ollama connection failed")
            return {"success": False, "error": "Ollama unavailable"}
        except httpx.TimeoutException:
            logger.warning("Ollama request timeout")
            return {"success": False, "error": "Ollama request timeout"}
        except Exception as e:
            logger.warning(f"Ollama inference failed")
            return {"success": False, "error": "Ollama inference failed"}


ollama_inference = OllamaInferenceService()
