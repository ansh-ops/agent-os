from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from app.agents.contracts import StructuredAgentOutput
from app.models.provider import BaseModelProvider, get_model_provider
from app.schemas.task import AgentName, AgentResult, TaskRecord
from app.tools.registry import ToolRegistry


@dataclass
class AgentContext:
    task: TaskRecord
    shared_facts: list[str]
    prior_outputs: list[AgentResult]


class BaseAgent(ABC):
    name: AgentName
    prompt: str
    capability_summary: str

    def __init__(self, model_provider: BaseModelProvider | None = None, tool_registry: ToolRegistry | None = None) -> None:
        self.model_provider = model_provider or get_model_provider()
        self.tool_registry = tool_registry or ToolRegistry()

    @abstractmethod
    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError

    def clip(self, text: str, *, limit: int = 160) -> str:
        cleaned = " ".join(text.split())
        return cleaned if len(cleaned) <= limit else f"{cleaned[: limit - 3]}..."

    def try_structured_completion(
        self,
        *,
        user_prompt: str,
        response_model: type[BaseModel],
    ) -> BaseModel | None:
        try:
            return self.model_provider.structured_completion(
                system_prompt=self.prompt,
                user_prompt=user_prompt,
                response_model=response_model,
            )
        except Exception:
            return None

    def result(
        self,
        summary: str,
        structured_output: StructuredAgentOutput | dict[str, Any],
        next_action: str | None = None,
    ) -> AgentResult:
        serialized_output = structured_output.model_dump() if isinstance(structured_output, BaseModel) else structured_output
        return AgentResult(
            agent=self.name,
            summary=summary,
            structured_output=serialized_output,
            suggested_next_action=next_action,
        )
