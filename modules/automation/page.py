"""Automation links, read-only GitHub status, and integration guidance."""

from __future__ import annotations

import streamlit as st

from modules.configuration import load_settings
from modules.automation.github import GitHubIntegrationError, fetch_workflow_runs


def render() -> None:
    st.header("Automation Centre")
    settings = load_settings()
    repository = st.text_input("GitHub repository (owner/name)", settings.github_repository)
    st.caption(
        "The status lookup is read-only. Public repositories can use the unauthenticated "
        "GitHub API subject to its rate limits; a token is optional for private repos or "
        "higher limits and must be provided as GITHUB_TOKEN in server environment/secrets."
    )
    if st.button("Fetch recent GitHub Actions runs"):
        try:
            runs = fetch_workflow_runs(repository, settings.github_token)
            if not runs:
                st.info("No workflow runs were returned.")
            for run in runs:
                st.write(
                    f"**{run.get('name') or run.get('display_title', 'Workflow')}** · "
                    f"{run.get('status', 'unknown')} / "
                    f"{run.get('conclusion') or 'in progress'} · "
                    f"{run.get('head_branch', 'unknown branch')}"
                )
                url = run.get("html_url")
                if isinstance(url, str) and url.startswith("https://github.com/"):
                    st.markdown(f"[Open run]({url})")
            st.session_state["recent_activities"].insert(0, "Checked GitHub Actions status")
        except GitHubIntegrationError as exc:
            st.error(str(exc))

    actions_url = f"https://github.com/{repository}/actions"
    if "/" in repository and " " not in repository:
        st.link_button("Open GitHub Actions", actions_url)

    st.subheader("Integration options")
    st.markdown(
        """
        - **Document processing:** CSV and XLSX ledger import is available in
          Accounting. PDF/OCR extraction is not connected.
        - **Scheduled workflows:** this repository includes a pytest GitHub Actions
          workflow. No scheduled or external-write workflows are enabled by this app.
        - **Free services:** public GitHub REST reads are available without a token,
          subject to GitHub's rate limits. Local processing does not require an API.
        - **Plan-dependent or paid services:** GitHub Actions quotas depend on account
          and repository plan; external AI and other API providers may charge usage.
        """
    )
    st.caption("No workflow dispatch, email, document upload, or external write is triggered here.")
