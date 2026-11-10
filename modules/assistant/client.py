"""Minimal OpenAI-compatible chat client with server-side credential handling."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class AssistantError(RuntimeError):
    """Raised for safe, user-presentable assistant integration failures."""


def ask_provider(
    prompt: str,
    *,
    api_key: str,
    base_url: str,
    model: str,
    timeout: int = 45,
) -> str:
    if not prompt.strip():
        raise AssistantError("Enter a question before sending it.")
    if len(prompt) > 6000:
        raise AssistantError("Questions must be 6,000 characters or fewer.")
    if not api_key.strip():
        raise AssistantError("No API key is configured.")
    parsed = urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise AssistantError("The provider URL must be an HTTPS URL without embedded credentials.")
    endpoint = base_url.rstrip("/") + "/chat/completions"
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an educational research assistant. Explain concepts "
                        "and suggest authoritative sources. Do not claim to provide "
                        "professional tax or legal advice. State uncertainty and ask "
                        "for the applicable jurisdiction and tax year when needed."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
    ).encode("utf-8")
    request = Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise AssistantError(
            f"The AI provider returned HTTP {exc.code}; check provider settings and quota."
        ) from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise AssistantError("Could not reach the configured AI provider.") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AssistantError("The AI provider returned an unreadable response.") from exc

    try:
        answer = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AssistantError("The AI provider response did not contain an answer.") from exc
    if not isinstance(answer, str) or not answer.strip():
        raise AssistantError("The AI provider returned an empty answer.")
    return answer.strip()
