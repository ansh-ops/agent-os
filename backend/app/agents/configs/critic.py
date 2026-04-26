from dataclasses import dataclass

from app.schemas.task import AgentName


@dataclass(frozen=True)
class CriticAgentConfig:
    name: AgentName = AgentName.CRITIC
    prompt: str = (
        "You are the critic agent for Agent OS. Review prior agent output for unsupported claims, "
        "missing detail, inconsistency, or weak recommendations, then return a quality verdict."
    )
    capability_summary: str = "Reviews specialist outputs and decides whether they are ready to present."


CRITIC_AGENT_CONFIG = CriticAgentConfig()
