from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from app.core.config import settings

T = TypeVar("T", bound=BaseModel)


class BaseModelProvider(ABC):
    @abstractmethod
    def structured_completion(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        raise NotImplementedError


class GeminiModelProvider(BaseModelProvider):
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash") -> None:
        self.api_key = api_key
        self.model_name = model_name

    def structured_completion(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Gemini support requires the `google-genai` package to be installed.") from exc

        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model=self.model_name,
            contents=f"System instructions:\n{system_prompt}\n\nUser request:\n{user_prompt}",
            config={
                "response_mime_type": "application/json",
                "response_json_schema": response_model.model_json_schema(),
            },
        )
        return response_model.model_validate(json.loads(response.text))


class OpenAIModelProvider(BaseModelProvider):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def structured_completion(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("OpenAI support requires the `openai` package to be installed.") from exc

        client = OpenAI(api_key=self.api_key)
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": response_model.__name__,
                    "schema": response_model.model_json_schema(),
                }
            },
        )
        return response_model.model_validate(json.loads(response.output_text))


class MockModelProvider(BaseModelProvider):
    def structured_completion(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        raise RuntimeError("Mock provider cannot generate arbitrary structured output.")


def get_model_provider() -> BaseModelProvider:
    if settings.use_mock_agents:
        return MockModelProvider()
    if settings.llm_provider == "gemini" and settings.gemini_api_key:
        return GeminiModelProvider(api_key=settings.gemini_api_key)
    if settings.llm_provider == "openai" and settings.openai_api_key:
        return OpenAIModelProvider(api_key=settings.openai_api_key)
    return MockModelProvider()
