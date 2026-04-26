from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class RuntimeMode(str, Enum):
    MOCK = "mock"
    LLM_ACTIVE = "llm_active"
    LLM_MISCONFIGURED = "llm_misconfigured"


class ProviderStatus(BaseModel):
    mode: RuntimeMode
    provider_key_present: bool
    mock_agents_enabled: bool
    sdk_installed: bool
    provider_reachable: bool
    provider_name: str
    last_error: str | None = None
