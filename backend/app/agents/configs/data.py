from dataclasses import dataclass

from app.schemas.task import AgentName


@dataclass(frozen=True)
class DataAgentConfig:
    name: AgentName = AgentName.DATA
    prompt: str = (
        "You are the data agent for Agent OS. Inspect uploaded CSV data, profile the schema, "
        "identify notable patterns or data quality risks, and recommend practical next steps."
    )
    capability_summary: str = "Reads CSV data and returns structured profiling plus next-step guidance."


DATA_AGENT_CONFIG = DataAgentConfig()
