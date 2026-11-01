from sqlalchemy import Column, String, DateTime, Text, JSON, Integer
from sqlalchemy.sql import func
from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="pending", index=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    task_metadata = Column(JSON, default=dict)


class AgentResponse(Base):
    __tablename__ = "agent_responses"

    id = Column(String, primary_key=True, index=True)
    task_id = Column(String, index=True)
    response = Column(Text)
    steps = Column(JSON, default=list)
    status = Column(String, default="completed")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, index=True)
    tool_name = Column(String)
    args = Column(JSON, default=dict)
    approved = Column(String, default="pending")
    status = Column(String, default="pending")
    result = Column(Text)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(String, primary_key=True, index=True)
    task_id = Column(String, index=True, nullable=True)
    tool_name = Column(String, nullable=False)
    tool_args = Column(JSON, default=dict)
    status = Column(String, default="pending", index=True)  # pending, approved, rejected, expired, used
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(String, nullable=True)
