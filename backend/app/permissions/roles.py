from __future__ import annotations

from enum import Enum

from app.schemas.task import AgentName


class Permission(str, Enum):
    READ_CONTEXT = "read_context"
    READ_CSV = "read_csv"
    READ_AGENT_OUTPUTS = "read_agent_outputs"
    WRITE_MEMORY = "write_memory"
    COORDINATE_WORKFLOW = "coordinate_workflow"
    REVIEW_OUTPUTS = "review_outputs"


AGENT_PERMISSIONS: dict[AgentName, set[Permission]] = {
    AgentName.SUPERVISOR: {
        Permission.READ_CONTEXT,
        Permission.READ_CSV,
        Permission.READ_AGENT_OUTPUTS,
        Permission.WRITE_MEMORY,
        Permission.COORDINATE_WORKFLOW,
        Permission.REVIEW_OUTPUTS,
    },
    AgentName.RESEARCH: {
        Permission.READ_CONTEXT,
        Permission.WRITE_MEMORY,
    },
    AgentName.DATA: {
        Permission.READ_CSV,
        Permission.WRITE_MEMORY,
    },
    AgentName.PLANNING: {
        Permission.READ_CONTEXT,
        Permission.READ_AGENT_OUTPUTS,
        Permission.WRITE_MEMORY,
    },
    AgentName.CRITIC: {
        Permission.READ_AGENT_OUTPUTS,
        Permission.REVIEW_OUTPUTS,
    },
}


def assert_permission(agent: AgentName, permission: Permission) -> None:
    if permission not in AGENT_PERMISSIONS.get(agent, set()):
        raise PermissionError(f"{agent.value} is not allowed to use {permission.value}")
