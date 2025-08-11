import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Literal, Optional

from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    parameters: Dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    taskId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    input: TaskInput = Field(default_factory=TaskInput)


class Error(BaseModel):
    code: str
    message: str


class Result(BaseModel):
    status: Literal["pending", "success", "failure"] = "pending"
    output: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[Error] = None


class Message(BaseModel):
    messageId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    fromAgent: str
    toAgent: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    task: Task
    result: Result = Field(default_factory=Result)
