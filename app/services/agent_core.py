from typing import Dict, Any, List
from loguru import logger

from app.services.task_planner import task_planner
from app.services.ollama_inference import ollama_inference


class AgentCore:
    async def process_task(self, task_description: str) -> Dict[str, Any]:
        steps = task_planner.plan(task_description)
        inference = await ollama_inference.generate(f"Task: {task_description}\nSteps: {steps}")
        if not inference.get("success"):
            return {
                "success": False,
                "error": inference.get("error", "Ollama unavailable"),
                "steps": steps,
            }
        return {
            "success": True,
            "response": inference.get("response", ""),
            "steps": steps,
            "model": inference.get("model"),
        }


agent_core = AgentCore()
