from typing import Dict, Any
from loguru import logger
from pathlib import Path
import os

from app.services.tool_registry import tool_registry
from app.services.permission_manager import permission_manager
from app.db.session import AsyncSessionLocal
from app.models.task import ExecutionLog
from app.services.workspace_guard import workspace_guard


class ToolExecutor:
    async def execute(self, task_id: str, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        tool = tool_registry.get_tool(tool_name)
        if not tool:
            async with AsyncSessionLocal() as session:
                log = ExecutionLog(task_id=task_id, tool_name=tool_name, args=args, status="failed", error_message="Tool not in allowlist")
                session.add(log)
                await session.commit()
            return {"success": False, "error": "Tool not in allowlist"}
        
        if not tool_registry.validate_args(tool_name, args):
            async with AsyncSessionLocal() as session:
                log = ExecutionLog(task_id=task_id, tool_name=tool_name, args=args, status="failed", error_message="Invalid arguments")
                session.add(log)
                await session.commit()
            return {"success": False, "error": "Invalid arguments"}
        
        # Enforce workspace restrictions for file operations
        if tool_name in ["read_file", "list_files", "search_files", "search_content", "create_note"]:
            if "path" in args:
                safe, result = workspace_guard.is_path_safe(args["path"])
                if not safe:
                    async with AsyncSessionLocal() as session:
                        log = ExecutionLog(task_id=task_id, tool_name=tool_name, args=args, status="failed", error_message="Access denied")
                        session.add(log)
                        await session.commit()
                    return {"success": False, "error": "Access denied"}
                args["path"] = result  # Use resolved safe path
        
        if tool.requires_approval:
            async with AsyncSessionLocal() as session:
                log = ExecutionLog(task_id=task_id, tool_name=tool_name, args=args, approved="pending", status="pending")
                session.add(log)
                await session.commit()
            return {"success": False, "requires_approval": True, "tool": tool_name, "args": args}
        
        # Execute non-approval tools (mocked/safe)
        async with AsyncSessionLocal() as session:
            log = ExecutionLog(task_id=task_id, tool_name=tool_name, args=args, approved="not_required", status="running")
            session.add(log)
            await session.commit()
            try:
                if tool_name == "read_file":
                    result = {"content": f"[mock] read {args.get('path')}"}
                elif tool_name == "list_files":
                    result = {"files": ["[mock] file1.txt"]}
                elif tool_name == "search_files":
                    result = {"files": ["[mock] match.txt"]}
                elif tool_name == "search_content":
                    result = {"matches": []}
                elif tool_name == "create_note":
                    result = {"note_id": "mock-note"}
                else:
                    result = {"status": "ok"}
                log.status = "completed"
                log.result = str(result)
                log.approved = "not_required"
                await session.commit()
                return {"success": True, "result": result}
            except Exception as e:
                log.status = "failed"
                log.error_message = "Tool execution failed"
                await session.commit()
                return {"success": False, "error": "Tool execution failed"}


tool_executor = ToolExecutor()
