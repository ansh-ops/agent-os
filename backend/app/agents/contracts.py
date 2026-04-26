from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ResearchOutput(BaseModel):
    task_goal: str
    findings: list[str]
    recommended_summary: str
    caveats: list[str]


class PlanningTaskItem(BaseModel):
    title: str
    owner: str
    status: str


class PlanningPhase(BaseModel):
    name: str
    deliverables: list[str]


class PlanningOutput(BaseModel):
    goal: str
    phases: list[PlanningPhase]
    task_tree: list[PlanningTaskItem]
    risks: list[str]
    next_steps: list[str]


class DataColumnProfile(BaseModel):
    column: str
    non_empty: int
    unique_values: int
    sample_values: list[str] = Field(default_factory=list)
    numeric_min: float | None = None
    numeric_max: float | None = None
    numeric_avg: float | None = None


class DataOutput(BaseModel):
    file_name: str | None = None
    row_count: int
    column_count: int
    columns: list[DataColumnProfile]
    observations: list[str]
    next_steps: list[str]


class CriticOutput(BaseModel):
    reviewed_agent: str
    issues: list[str]
    recommendation: str
    quality_score: float


StructuredAgentOutput = ResearchOutput | PlanningOutput | DataOutput | CriticOutput
