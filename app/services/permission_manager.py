from typing import Dict, Any, Tuple, Optional
from app.services.tool_registry import tool_registry
from app.db.session import AsyncSessionLocal
from app.models.task import ApprovalRequest
from loguru import logger
import uuid
from datetime import datetime


class PermissionManager:
    def __init__(self):
        self._pending_approvals: Dict[str, Dict[str, Any]] = {}

    def validate_tool_call(self, tool_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        tool = tool_registry.get_tool(tool_name)
        if not tool:
            logger.warning("Attempted to call unregistered tool")
            return False, "Tool not in allowlist"
        if not tool_registry.is_allowed(tool_name):
            return False, "Tool not allowed"
        if tool_name in ["read_file", "list_files"]:
            if "path" not in args or not isinstance(args.get("path"), str):
                return False, "Invalid or missing argument: path"
        if tool.requires_approval:
            return False, "Tool requires explicit user approval"
        return True, "OK"

    async def create_approval_request(self, tool_name: str, args: Dict[str, Any], task_id: Optional[str] = None) -> str:
        request_id = str(uuid.uuid4())
        async with AsyncSessionLocal() as session:
            approval = ApprovalRequest(
                id=request_id,
                task_id=task_id,
                tool_name=tool_name,
                tool_args=args,
                status="pending",
            )
            session.add(approval)
            await session.commit()
        logger.info("Approval request created")
        return request_id

    async def approve_request(self, request_id: str) -> Tuple[bool, str]:
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(select(ApprovalRequest).where(ApprovalRequest.id == request_id))
            approval = result.scalars().first()
            if not approval:
                return False, "Approval request not found"
            if approval.status != "pending":
                return False, f"Approval request already {approval.status}"
            approval.status = "approved"
            approval.resolved_at = datetime.utcnow()
            approval.resolved_by = "user"
            await session.commit()
            return True, "Approved"

    async def reject_request(self, request_id: str) -> Tuple[bool, str]:
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(select(ApprovalRequest).where(ApprovalRequest.id == request_id))
            approval = result.scalars().first()
            if not approval:
                return False, "Approval request not found"
            if approval.status != "pending":
                return False, f"Approval request already {approval.status}"
            approval.status = "rejected"
            approval.resolved_at = datetime.utcnow()
            approval.resolved_by = "user"
            await session.commit()
            return True, "Rejected"

    async def validate_approved_request(self, request_id: str, tool_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(select(ApprovalRequest).where(ApprovalRequest.id == request_id))
            approval = result.scalars().first()
            if not approval:
                return False, "Approval request not found"
            if approval.status != "approved":
                return False, "Approval not granted"
            if approval.status == "used":
                return False, "Approval already used"
            if approval.tool_name != tool_name:
                return False, "Tool name mismatch"
            if approval.tool_args != args:
                return False, "Arguments mismatch"
            approval.status = "used"
            await session.commit()
            return True, "OK"


permission_manager = PermissionManager()
