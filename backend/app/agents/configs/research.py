from dataclasses import dataclass

from app.schemas.task import AgentName


@dataclass(frozen=True)
class ResearchAgentConfig:
    name: AgentName = AgentName.RESEARCH
    prompt: str = (
        "You are the research agent for Agent OS. Use only the task prompt and internal context, "
        "extract key findings, summarize them clearly, and surface any evidence limitations."
    )
    capability_summary: str = "Reads text context and produces structured research findings."


RESEARCH_AGENT_CONFIG = ResearchAgentConfig()
