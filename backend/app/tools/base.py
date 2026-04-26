from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from app.permissions.roles import Permission, assert_permission
from app.schemas.task import AgentName, TaskRecord


@dataclass
class ToolInvocationContext:
    agent: AgentName
    task: TaskRecord


class BaseTool(ABC):
    name: str
    required_permission: Permission

    def invoke(self, context: ToolInvocationContext, **kwargs: Any) -> Any:
        assert_permission(context.agent, self.required_permission)
        return self._invoke(context, **kwargs)

    @abstractmethod
    def _invoke(self, context: ToolInvocationContext, **kwargs: Any) -> Any:
        raise NotImplementedError
