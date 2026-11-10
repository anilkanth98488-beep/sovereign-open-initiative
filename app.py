from __future__ import annotations

import streamlit as st

from modules.accounting.page import render as render_accounting
from modules.assistant.page import render as render_assistant
from modules.automation.page import render as render_automation
from modules.career.page import render as render_career
from modules.dashboard import render as render_dashboard
from modules.learning.page import render as render_learning
from modules.tax_center import render as render_tax_center

NAVIGATION = (
    "Dashboard",
    "Accounting",
    "US & Canadian Tax",
    "Learning & VITA",
    "Career",
    "AI Assistant",
    "Automation",
)

st.set_page_config(
    page_title="Sovereign OS | Professional Workspace",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
    .block-container { padding-top: 1.8rem; }
    [data-testid="stSidebar"] { border-right: 1px solid rgba(128, 128, 128, .18); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.session_state.setdefault("recent_activities", [])
st.session_state.setdefault("workspace_navigation", "Dashboard")
with st.sidebar:
    st.title("🦅 Sovereign OS")
    st.caption("Professional workspace · Preview")
    st.radio("Workspace", NAVIGATION, key="workspace_navigation")
    st.divider()
    st.caption("Use synthetic data only. AI and external integrations are opt-in.")

page = st.session_state["workspace_navigation"]
if page == "Dashboard":
    render_dashboard()
elif page == "Accounting":
    render_accounting()
elif page == "US & Canadian Tax":
    render_tax_center()
elif page == "Learning & VITA":
    render_learning()
elif page == "Career":
    render_career()
elif page == "AI Assistant":
    render_assistant()
elif page == "Automation":
    render_automation()
