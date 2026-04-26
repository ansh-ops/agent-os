from __future__ import annotations

from app.core.config import settings
from app.schemas.system import ProviderStatus, RuntimeMode


class SystemStatusService:
    def get_provider_status(self) -> ProviderStatus:
        provider_name = settings.llm_provider
        key_present = bool(settings.gemini_api_key) if provider_name == "gemini" else bool(settings.openai_api_key)
        mock_enabled = settings.use_mock_agents

        try:
            if provider_name == "gemini":
                from google import genai  # noqa: F401
            else:
                import openai  # noqa: F401
            sdk_installed = True
        except ImportError:
            sdk_installed = False

        if mock_enabled:
            return ProviderStatus(
                mode=RuntimeMode.MOCK,
                provider_key_present=key_present,
                mock_agents_enabled=mock_enabled,
                sdk_installed=sdk_installed,
                provider_reachable=False,
                provider_name="mock",
            )

        if not key_present:
            return ProviderStatus(
                mode=RuntimeMode.LLM_MISCONFIGURED,
                provider_key_present=False,
                mock_agents_enabled=mock_enabled,
                sdk_installed=sdk_installed,
                provider_reachable=False,
                provider_name=provider_name,
                last_error="GEMINI_API_KEY is missing." if provider_name == "gemini" else "OPENAI_API_KEY is missing.",
            )

        if not sdk_installed:
            return ProviderStatus(
                mode=RuntimeMode.LLM_MISCONFIGURED,
                provider_key_present=key_present,
                mock_agents_enabled=mock_enabled,
                sdk_installed=False,
                provider_reachable=False,
                provider_name=provider_name,
                last_error=(
                    "The `google-genai` package is not installed in the backend environment."
                    if provider_name == "gemini"
                    else "The `openai` package is not installed in the backend environment."
                ),
            )

        try:
            if provider_name == "gemini":
                from google import genai

                client = genai.Client(api_key=settings.gemini_api_key)
                next(iter(client.models.list()))
            else:
                from openai import OpenAI

                client = OpenAI(api_key=settings.openai_api_key)
                client.models.list()
            return ProviderStatus(
                mode=RuntimeMode.LLM_ACTIVE,
                provider_key_present=key_present,
                mock_agents_enabled=mock_enabled,
                sdk_installed=True,
                provider_reachable=True,
                provider_name=provider_name,
            )
        except Exception as exc:
            return ProviderStatus(
                mode=RuntimeMode.LLM_MISCONFIGURED,
                provider_key_present=key_present,
                mock_agents_enabled=mock_enabled,
                sdk_installed=True,
                provider_reachable=False,
                provider_name=provider_name,
                last_error=str(exc),
            )
