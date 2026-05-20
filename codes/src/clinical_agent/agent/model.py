from __future__ import annotations
from typing import Any
from langchain_openai import AzureChatOpenAI
from clinical_agent.config import get_settings
from clinical_agent.agent.json_utils import extract_json_object


def get_azure_chat_model(temperature: float = 0.0):
    settings = get_settings()
    if not settings.azure_openai_endpoint or not settings.azure_openai_api_key or not settings.azure_openai_deployment:
        raise RuntimeError("Azure OpenAI configuration is incomplete.")
    return AzureChatOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        azure_deployment=settings.azure_openai_deployment,
        api_version=settings.azure_openai_api_version,
        temperature=temperature,
    )


def optional_json_classification(prompt: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.use_azure_openai_triage:
        return {}
    try:
        llm = get_azure_chat_model(temperature=0.0)
        response = llm.invoke(prompt)
        return extract_json_object(getattr(response, "content", str(response)))
    except Exception:
        return {}


def optional_text_generation(prompt: str) -> str | None:
    settings = get_settings()
    if not settings.use_azure_openai_response:
        return None
    try:
        llm = get_azure_chat_model(temperature=0.2)
        response = llm.invoke(prompt)
        return getattr(response, "content", str(response))
    except Exception:
        return None
