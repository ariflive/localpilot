from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    task_metadata: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class TaskDetail(TaskResponse):
    steps: List[Dict[str, Any]] = []
    agent_response: Optional[str] = None
    agent_error: Optional[str] = None


class AgentRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class ApprovalRequestCreate(BaseModel):
    tool_name: str = Field(..., min_length=1)
    tool_args: Dict[str, Any] = Field(default_factory=dict)
    task_id: Optional[str] = None


class ApprovalResponse(BaseModel):
    action: str = Field(..., pattern="^(approve|reject)$")
