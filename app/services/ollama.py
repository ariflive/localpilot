import httpx
from loguru import logger

from app.core.config import settings


class OllamaService:
    def __init__(self):
        self.base_url = settings.ollama_base_url

    async def check_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/version")
                if response.status_code == 200:
                    logger.info(f"Ollama connected: {response.json()}")
                    return True
                logger.warning(f"Ollama returned status {response.status_code}")
                return False
        except Exception as e:
            logger.warning(f"Ollama connection failed: {e}")
            return False


ollama_service = OllamaService()
