from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.db.session import get_db, AsyncSessionLocal
from app.models.task import Task, AgentResponse, ApprovalRequest, ExecutionLog
from app.schemas.task import TaskCreate, TaskResponse, TaskDetail, ApprovalRequestCreate, ApprovalResponse
from app.services.agent_core import agent_core
from app.services.permission_manager import permission_manager
from app.services.tool_executor import tool_executor

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db)):
    task_id = str(uuid.uuid4())
    db_task = Task(id=task_id, title=task_in.title, description=task_in.description, status="processing")
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    try:
        result = await agent_core.process_task(task_id, task_in.description)
        if result.get("requires_approval"):
            db_task.status = "pending_approval"
            await db.commit()
            await db.refresh(db_task)
            return db_task
        if result.get("success"):
            agent_resp = AgentResponse(
                id=str(uuid.uuid4()),
                task_id=task_id,
                response=result.get("response", ""),
                steps=result.get("steps", []),
                status="completed",
            )
            db.add(agent_resp)
            db_task.status = "completed"
            db_task.error_message = None
        else:
            db_task.status = "failed"
            error_msg = result.get("error", "Task processing failed")
            db_task.error_message = error_msg
            agent_resp = AgentResponse(
                id=str(uuid.uuid4()),
                task_id=task_id,
                response="",
                steps=result.get("steps", []),
                status="failed",
                error_message=error_msg,
            )
            db.add(agent_resp)
    except Exception as e:
        db_task.status = "failed"
        error_msg = "Internal processing error"
        db_task.error_message = error_msg
        agent_resp = AgentResponse(
            id=str(uuid.uuid4()),
            task_id=task_id,
            response="",
            steps=[],
            status="failed",
            error_message=error_msg,
        )
        db.add(agent_resp)
    await db.commit()
    await db.refresh(db_task)
    return db_task


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).order_by(Task.created_at.desc()))
    tasks = result.scalars().all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskDetail)
async def get_task(task_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    resp_result = await db.execute(select(AgentResponse).where(AgentResponse.task_id == task_id))
    agent_resp = resp_result.scalars().first()
    detail = TaskDetail.model_validate(task)
    if agent_resp:
        detail.agent_response = agent_resp.response if agent_resp.response else None
        detail.steps = agent_resp.steps or []
        detail.agent_error = agent_resp.error_message
    return detail


@router.post("/approvals")
async def create_approval(approval_in: ApprovalRequestCreate):
    request_id = await permission_manager.create_approval_request(
        approval_in.tool_name, approval_in.tool_args, approval_in.task_id
    )
    return {"approval_id": request_id, "status": "pending"}


@router.get("/approvals")
async def list_approvals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ApprovalRequest).order_by(ApprovalRequest.created_at.desc()))
    approvals = result.scalars().all()
    return [
        {
            "id": a.id,
            "task_id": a.task_id,
            "tool_name": a.tool_name,
            "tool_args": a.tool_args,
            "status": a.status,
            "created_at": a.created_at,
            "resolved_at": a.resolved_at,
        }
        for a in approvals
    ]


@router.post("/approvals/{approval_id}/respond")
async def respond_approval(approval_id: str, response: ApprovalResponse):
    if response.action == "approve":
        success, msg = await permission_manager.approve_request(approval_id)
        if not success:
            raise HTTPException(status_code=400, detail=msg)
        # Execute approved tool
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(select(ApprovalRequest).where(ApprovalRequest.id == approval_id))
            approval = result.scalars().first()
            if approval and approval.task_id:
                exec_result = await tool_executor.execute(approval.task_id, approval.tool_name, approval.tool_args)
                if exec_result.get("success"):
                    # Mark task completed
                    r2 = await session.execute(select(Task).where(Task.id == approval.task_id))
                    task = r2.scalars().first()
                    if task:
                        task.status = "completed"
                    agent_resp = AgentResponse(
                        id=str(uuid.uuid4()),
                        task_id=approval.task_id,
                        response="Tool executed successfully",
                        steps=[],
                        status="completed",
                    )
                    session.add(agent_resp)
                    await session.commit()
                else:
                    r2 = await session.execute(select(Task).where(Task.id == approval.task_id))
                    task = r2.scalars().first()
                    if task:
                        task.status = "failed"
                    await session.commit()
        return {"approval_id": approval_id, "status": "approved"}
    elif response.action == "reject":
        success, msg = await permission_manager.reject_request(approval_id)
        if not success:
            raise HTTPException(status_code=400, detail=msg)
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(select(ApprovalRequest).where(ApprovalRequest.id == approval_id))
            approval = result.scalars().first()
            if approval and approval.task_id:
                r2 = await session.execute(select(Task).where(Task.id == approval.task_id))
                task = r2.scalars().first()
                if task:
                    task.status = "rejected"
                await session.commit()
        return {"approval_id": approval_id, "status": "rejected"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
