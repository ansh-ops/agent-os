from dataclasses import dataclass

from app.schemas.task import AgentName


@dataclass(frozen=True)
class PlanningAgentConfig:
    name: AgentName = AgentName.PLANNING
    prompt: str = (
        "You are the planning agent for Agent OS. Translate goals into phased execution plans, "
        "task trees, dependencies, and practical next actions that a builder can immediately follow."
    )
    capability_summary: str = "Turns high-level goals into structured plans and task checklists."


PLANNING_AGENT_CONFIG = PlanningAgentConfig()
