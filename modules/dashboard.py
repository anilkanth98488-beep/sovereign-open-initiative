"""Workspace overview, local health checks, and quick navigation."""

from __future__ import annotations

import platform
from pathlib import Path

import pandas as pd
import streamlit as st

from modules.configuration import load_settings

MODULES = (
    ("Accounting", "Ready"),
    ("US & Canadian Tax Centre", "Educational workpapers"),
    ("Learning & VITA", "Ready"),
    ("Career Centre", "Session-only"),
    ("AI Assistant", "Optional provider"),
    ("Automation Centre", "Optional integrations"),
)


def _navigate(destination: str) -> None:
    st.session_state["workspace_navigation"] = destination


def render() -> None:
    st.header("Sovereign OS · Professional Workspace")
    st.write(
        "A modular workspace for synthetic-data accounting demonstrations, tax-learning "
        "workpapers, career development, and optional integrations."
    )
    sample_path = Path(__file__).resolve().parents[1] / "sample_data" / "synthetic_ledger.csv"
    settings = load_settings()
    health = st.columns(4)
    health[0].metric("Workspace", "Online")
    health[1].metric("Python", platform.python_version())
    health[2].metric("Sample ledger", "Available" if sample_path.is_file() else "Missing")
    health[3].metric("AI provider", "Configured" if settings.ai_api_key else "Optional")

    st.subheader("Module status")
    status_columns = st.columns(3)
    for index, (name, status) in enumerate(MODULES):
        with status_columns[index % len(status_columns)]:
            st.metric(name, status)

    st.subheader("Quick access")
    destinations = (
        ("Open Accounting", "Accounting"),
        ("Open Tax Centre", "US & Canadian Tax"),
        ("Open Learning", "Learning & VITA"),
        ("Open Career Centre", "Career"),
        ("Open AI Assistant", "AI Assistant"),
        ("Open Automation", "Automation"),
    )
    quick_columns = st.columns(3)
    for index, (label, destination) in enumerate(destinations):
        quick_columns[index % 3].button(
            label,
            key=f"quick_{destination}",
            on_click=_navigate,
            args=(destination,),
        )

    st.subheader("Recent activities")
    activities = st.session_state.get("recent_activities", [])
    if activities:
        for activity in activities[:8]:
            st.write(f"- {activity}")
    else:
        st.info("Activities from this browser session will appear here.")
    st.caption(
        f"Loaded with Streamlit {st.__version__} and pandas {pd.__version__}. "
        "Status checks describe local application readiness, not external tax or audit assurance."
    )
