"""Opt-in AI assistance with credential and data-sharing disclosure."""

from __future__ import annotations

import streamlit as st

from modules.configuration import load_settings
from modules.assistant.client import AssistantError, ask_provider


def render() -> None:
    st.header("AI Assistant")
    st.warning(
        "Optional external service. Do not submit client, taxpayer, identity, financial, "
        "or other confidential data. Prompts are sent to the configured provider only "
        "after you submit; that provider's terms and retention policies apply."
    )
    settings = load_settings()
    st.selectbox("Provider", ("OpenAI-compatible chat API",))
    base_url = st.text_input("Provider base URL", value=settings.ai_base_url)
    model = st.text_input("Model", value=settings.ai_model)
    if settings.ai_api_key:
        api_key = settings.ai_api_key
        st.success("API key configured in environment or Streamlit secrets; value is hidden.")
    else:
        api_key = st.text_input(
            "API key (optional; kept only in this session)",
            type="password",
            help="Prefer SOVEREIGN_AI_API_KEY in environment variables or Streamlit secrets.",
        )
        st.caption("No key is required to use the rest of the workspace.")

    assistant_task = st.selectbox(
        "Assistance type",
        (
            "Research assistance",
            "Tax document explanation",
            "Accounting explanation",
            "Learning assistance",
        ),
    )
    prompt = st.text_area(
        "Question",
        max_chars=5800,
        placeholder="Ask a general question. Include jurisdiction and tax year where relevant.",
    )
    confirmed = st.checkbox(
        "I have removed confidential information and approve sending this prompt to the configured provider."
    )
    if st.button("Send question", type="primary"):
        if not confirmed:
            st.error("Confirm the data-sharing notice before sending a prompt.")
        elif not api_key:
            st.error("Configure a provider key in the environment/secrets or this session.")
        else:
            try:
                with st.spinner("Waiting for the configured provider…"):
                    answer = ask_provider(
                        f"Assistance type: {assistant_task}\n\n{prompt}",
                        api_key=api_key,
                        base_url=base_url,
                        model=model,
                    )
                st.markdown(answer)
                st.caption("Verify responses against official sources; AI output can be inaccurate.")
                st.session_state["recent_activities"].insert(0, "Used optional AI assistant")
            except AssistantError as exc:
                st.error(str(exc))
