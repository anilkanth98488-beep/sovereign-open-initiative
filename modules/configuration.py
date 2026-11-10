"""Application configuration shared by the UI integration modules."""

from __future__ import annotations

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from core.config import Settings


def load_settings() -> Settings:
    try:
        return Settings.load(st.secrets)
    except (FileNotFoundError, StreamlitSecretNotFoundError):
        return Settings.load()
