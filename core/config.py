"""Environment-backed configuration for optional integrations."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Settings:
    github_repository: str
    github_token: str | None
    ai_api_key: str | None
    ai_base_url: str
    ai_model: str

    @classmethod
    def load(cls, secrets: Mapping[str, object] | None = None) -> "Settings":
        def value(name: str, default: str = "") -> str:
            configured = os.getenv(name)
            if configured:
                return configured.strip()
            if secrets is not None:
                secret = secrets.get(name)
                if isinstance(secret, str) and secret.strip():
                    return secret.strip()
            return default

        return cls(
            github_repository=value(
                "SOVEREIGN_GITHUB_REPOSITORY",
                "anilkanth98488-beep/sovereign-open-initiative",
            ),
            github_token=value("GITHUB_TOKEN") or None,
            ai_api_key=value("SOVEREIGN_AI_API_KEY") or None,
            ai_base_url=value("SOVEREIGN_AI_BASE_URL", "https://api.openai.com/v1"),
            ai_model=value("SOVEREIGN_AI_MODEL", "gpt-4o-mini"),
        )
