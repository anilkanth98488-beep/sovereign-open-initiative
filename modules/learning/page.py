"""Interactive learning tracks, practice, and session-only progress."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modules.learning.catalog import LEARNING_TRACKS, PRACTICE_QUESTIONS


def render() -> None:
    st.header("Learning & VITA Centre")
    st.caption(
        "Original study prompts and planning aids; not official IRS, CRA, EA, or CPA exam content."
    )
    track = st.selectbox("Learning track", list(LEARNING_TRACKS))
    st.subheader(track)
    progress_key = f"learning_progress_{track}"
    completed = set(st.session_state.get(progress_key, []))
    for item in LEARNING_TRACKS[track]:
        checked = st.checkbox(
            item,
            value=item in completed,
            key=f"{progress_key}_{item}",
        )
        if checked:
            completed.add(item)
        else:
            completed.discard(item)
    st.session_state[progress_key] = sorted(completed)
    st.progress(len(completed) / len(LEARNING_TRACKS[track]))
    st.caption(f"{len(completed)} of {len(LEARNING_TRACKS[track])} steps completed · current browser session only")

    st.divider()
    st.subheader("Practice question")
    question = st.selectbox("Choose a question", list(PRACTICE_QUESTIONS))
    item = PRACTICE_QUESTIONS[question]
    choice = st.radio("Select an answer", item["options"], key=f"practice_{question}")
    if st.button("Check answer", key="check_learning_answer"):
        if choice == item["answer"]:
            st.success("Correct. " + item["explanation"])
        else:
            st.warning("Not quite. " + item["explanation"])

    progress_rows = [
        {"Track": name, "Completed": len(st.session_state.get(f"learning_progress_{name}", [])),
         "Total": len(steps)}
        for name, steps in LEARNING_TRACKS.items()
    ]
    progress = pd.DataFrame(progress_rows)
    st.download_button(
        "Download learning progress (CSV)",
        data=progress.to_csv(index=False),
        file_name="learning-progress.csv",
        mime="text/csv",
    )
