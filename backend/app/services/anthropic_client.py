"""
Shared Anthropic API client.
Handles the Anthropic Messages API format which differs from OpenAI:
  - Endpoint: POST https://api.anthropic.com/v1/messages
  - Auth header: x-api-key (not Authorization: Bearer)
  - Required header: anthropic-version
  - System prompt is a top-level field, not a message role
  - Response: content[0].text (not choices[0].message.content)
"""
from __future__ import annotations

import httpx

from app.config import settings
from app.models.schemas import AIServiceError, AITimeoutError

ANTHROPIC_VERSION = "2023-06-01"
MAX_TOKENS = 4096


async def call_anthropic(
    messages: list[dict],
    system: str | None = None,
    temperature: float = 0.3,
) -> str:
    """
    Call the Anthropic Messages API.

    Args:
        messages: List of {"role": "user"|"assistant", "content": str} dicts.
                  Do NOT include system messages here — pass them via `system`.
        system:   Optional system prompt string.
        temperature: Sampling temperature (0.0–1.0).

    Returns:
        The assistant's reply as a plain string.

    Raises:
        AITimeoutError: If the request times out.
        AIServiceError: If the API returns an error or unparseable response.
    """
    headers = {
        "x-api-key": settings.AI_API_KEY,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }

    payload: dict = {
        "model": settings.AI_MODEL,
        "max_tokens": MAX_TOKENS,
        "temperature": temperature,
        "messages": messages,
    }
    if system:
        payload["system"] = system

    try:
        async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT_SECONDS) as client:
            response = await client.post(settings.AI_API_URL, json=payload, headers=headers)
    except httpx.TimeoutException:
        raise AITimeoutError("AI provider did not respond within the timeout period.")

    if response.status_code != 200:
        try:
            err = response.json()
            detail = err.get("error", {}).get("message", f"HTTP {response.status_code}")
        except Exception:
            detail = f"HTTP {response.status_code}"
        raise AIServiceError(f"Anthropic API error: {detail}")

    try:
        data = response.json()
        return data["content"][0]["text"]
    except Exception as exc:
        raise AIServiceError(f"Failed to parse Anthropic response: {exc}") from exc
