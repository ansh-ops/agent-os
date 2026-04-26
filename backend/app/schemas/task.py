from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TaskType(str, Enum):
    AUTO = "auto"
    RESEARCH = "research"
    DATA = "data"
    PLANNING = "planning"


class TaskStatus(str, Enum):
    QUEUED = "queued"
    PLANNING = "planning"
    RUNNING = "running"
    WAITING_ON_AGENT = "waiting_on_agent"
    UNDER_REVIEW = "under_review"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentName(str, Enum):
    SUPERVISOR = "supervisor"
    RESEARCH = "research_agent"
    DATA = "data_agent"
    PLANNING = "planning_agent"
    CRITIC = "critic_agent"


class TraceStatus(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


class MemoryEntryType(str, Enum):
    TASK_SUMMARY = "task_summary"
    EXTRACTED_FACT = "extracted_fact"
    AGENT_OUTPUT = "agent_output"
    EXECUTION_EVENT = "execution_event"
    FINAL_ARTIFACT = "final_artifact"


class ArtifactType(str, Enum):
    TEXT = "text"
    JSON = "json"


class TraceEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    agent: AgentName
    step_name: str
    prompt_summary: str
    status: TraceStatus
    created_at: datetime = Field(default_factory=utc_now)
    started_at: datetime = Field(default_factory=utc_now)
    finished_at: datetime | None = None
    output_summary: str | None = None
    error: str | None = None


class MemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: MemoryEntryType
    title: str
    content: str
    source_agent: AgentName | None = None
    created_at: datetime = Field(default_factory=utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskArtifact(BaseModel):
    name: str
    artifact_type: ArtifactType
    content: str
    created_at: datetime = Field(default_factory=utc_now)


class AgentResult(BaseModel):
    agent: AgentName
    summary: str
    structured_output: dict[str, Any]
    suggested_next_action: str | None = None


class TaskCreate(BaseModel):
    prompt: str = Field(min_length=3)
    task_type: TaskType = TaskType.AUTO
    context_text: str | None = None


class TaskRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    prompt: str
    task_type: TaskType
    inferred_task_type: TaskType | None = None
    status: TaskStatus = TaskStatus.QUEUED
    uploaded_file_name: str | None = None
    uploaded_file_path: str | None = None
    uploaded_file_type: str | None = None
    uploaded_file_text: str | None = None
    uploaded_file_error: str | None = None
    context_text: str | None = None
    result: str | None = None
    result_sections: list[dict[str, Any]] = Field(default_factory=list)
    artifacts: list[TaskArtifact] = Field(default_factory=list)
    traces: list[TraceEntry] = Field(default_factory=list)
    memory: list[MemoryEntry] = Field(default_factory=list)
    agent_outputs: list[AgentResult] = Field(default_factory=list)
    error: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class TaskListItem(BaseModel):
    id: str
    prompt: str
    task_type: TaskType
    inferred_task_type: TaskType | None = None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


class TaskCollection(BaseModel):
    items: list[TaskListItem]


class TaskDownloadResponse(BaseModel):
    task_id: str
    format: ArtifactType
    content: str
