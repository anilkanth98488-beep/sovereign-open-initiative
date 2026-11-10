"""Read-only GitHub Actions status integration."""

from __future__ import annotations

import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class GitHubIntegrationError(RuntimeError):
    """Raised for invalid repository names or GitHub API failures."""


REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def fetch_workflow_runs(
    repository: str, token: str | None = None, timeout: int = 15
) -> list[dict]:
    if not REPOSITORY_PATTERN.fullmatch(repository):
        raise GitHubIntegrationError("Enter a repository as owner/name.")
    request = Request(
        f"https://api.github.com/repos/{repository}/actions/runs?per_page=5",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise GitHubIntegrationError(
            f"GitHub returned HTTP {exc.code}; check repository visibility and API limits."
        ) from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise GitHubIntegrationError("Could not reach the GitHub API.") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GitHubIntegrationError("GitHub returned an unreadable response.") from exc

    runs = result.get("workflow_runs") if isinstance(result, dict) else None
    if not isinstance(runs, list):
        raise GitHubIntegrationError("GitHub response did not contain workflow runs.")
    return runs
