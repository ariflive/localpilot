from typing import Dict, Any, List
from loguru import logger

from app.services.task_planner import task_planner
from app.services.ollama_inference import ollama_inference
from app.services.tool_registry import tool_registry
from app.services.permission_manager import permission_manager
from app.services.tool_executor import tool_executor
from app.db.session import AsyncSessionLocal
from app.models.task import ApprovalRequest


class AgentCore:
    async def process_task(self, task_id: str, task_description: str) -> Dict[str, Any]:
        steps = task_planner.plan(task_description)
        desc_lower = task_description.lower()
        
        # Check if web_search is needed
        if "search the web" in desc_lower or ("web" in desc_lower and "search" in desc_lower):
            tool = tool_registry.get_tool("web_search")
            if tool and tool.requires_approval:
                # Create approval request
                approval_id = await permission_manager.create_approval_request("web_search", {"query": task_description}, task_id)
                async with AsyncSessionLocal() as session:
                    from sqlalchemy import select
                    result = await session.execute(select(ApprovalRequest).where(ApprovalRequest.id == approval_id))
                    approval = result.scalars().first()
                return {
                    "success": False,
                    "requires_approval": True,
                    "approval_id": approval_id,
                    "tool": "web_search",
                    "args": {"query": task_description},
                    "steps": steps,
                    "status": "pending_approval"
                }
        
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
