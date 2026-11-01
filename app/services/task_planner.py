from typing import List, Dict, Any
from loguru import logger


class TaskPlanner:
    def plan(self, description: str) -> List[Dict[str, Any]]:
        # Simple deterministic planner
        steps = []
        desc_lower = description.lower()
        if "search" in desc_lower or "find" in desc_lower:
            steps.append({"step": 1, "action": "search_files", "description": "Locate relevant files"})
        steps.append({"step": len(steps) + 1, "action": "analyze", "description": "Analyze requirements"})
        steps.append({"step": len(steps) + 1, "action": "respond", "description": "Provide structured response"})
        logger.info(f"Planned {len(steps)} steps")
        return steps


task_planner = TaskPlanner()
