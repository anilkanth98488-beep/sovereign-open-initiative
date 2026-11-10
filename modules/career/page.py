"""Session-only resume, skills, job application, and career plan tools."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import streamlit as st

SKILLS = (
    "US individual tax concepts",
    "US partnership and S corporation concepts",
    "Canadian T1 and T2 concepts",
    "GST/HST bookkeeping",
    "Ledger reconciliation",
    "Tax research and source documentation",
    "Client communication",
    "Spreadsheet and workpaper quality review",
)
CAREER_PLAN = (
    "Choose a target role and jurisdiction",
    "Map current skills to role requirements",
    "Complete a relevant learning module",
    "Prepare a work sample using synthetic data",
    "Review resume and interview examples",
)


def render() -> None:
    st.header("Career Centre")
    st.info(
        "Resume files, skills, and job records are held in Streamlit session memory only. "
        "They are not saved to a database or disk by this application; use synthetic or "
        "redacted material in hosted environments."
    )

    with st.expander("Resume library", expanded=True):
        uploader_key = f"career_resume_{st.session_state.get('resume_uploader_generation', 0)}"
        uploaded = st.file_uploader(
            "Add a resume file", type=["pdf", "docx", "txt"], key=uploader_key
        )
        if uploaded is not None:
            content = uploaded.getvalue()
            if len(content) > 10 * 1024 * 1024:
                st.error("Resume files must be 10 MB or smaller.")
            else:
                digest = hashlib.sha256(content).hexdigest()
                resumes = st.session_state.setdefault("career_resumes", {})
                resumes.setdefault(
                    digest,
                    {
                        "name": Path(uploaded.name).name,
                        "size": len(content),
                        "content": content,
                    },
                )
        for digest, resume in st.session_state.get("career_resumes", {}).items():
            columns = st.columns([3, 1, 1])
            columns[0].write(f"{resume['name']} · {resume['size']:,} bytes")
            columns[1].download_button(
                "Download",
                data=resume["content"],
                file_name=resume["name"],
                key=f"download_resume_{digest}",
            )
            if columns[2].button("Remove", key=f"remove_resume_{digest}"):
                del st.session_state["career_resumes"][digest]
                st.session_state["resume_uploader_generation"] = (
                    st.session_state.get("resume_uploader_generation", 0) + 1
                )
                st.rerun()

    st.subheader("Skills tracker")
    skill_state = st.session_state.setdefault("career_skills", {})
    skill_columns = st.columns(2)
    for index, skill in enumerate(SKILLS):
        skill_state[skill] = skill_columns[index % 2].checkbox(
            skill, value=skill_state.get(skill, False), key=f"skill_{skill}"
        )
    mastered = sum(skill_state.values())
    st.progress(mastered / len(SKILLS))
    st.caption(f"{mastered} of {len(SKILLS)} skills marked as developed")

    st.subheader("Job application tracker")
    starter = pd.DataFrame(
        [
            {
                "Company": "",
                "Role": "",
                "Jurisdiction": "",
                "Status": "",
                "Applied date": "",
                "Next step": "",
            }
        ]
    )
    jobs = st.data_editor(
        starter,
        key="career_job_applications",
        num_rows="dynamic",
        hide_index=True,
    )
    st.download_button(
        "Download job tracker (CSV)",
        data=jobs.to_csv(index=False),
        file_name="job-application-tracker.csv",
        mime="text/csv",
    )

    st.subheader("Career development plan")
    plan_state = st.session_state.setdefault("career_plan", {})
    for item in CAREER_PLAN:
        plan_state[item] = st.checkbox(
            item, value=plan_state.get(item, False), key=f"career_plan_{item}"
        )
    completed = sum(plan_state.values())
    st.progress(completed / len(CAREER_PLAN))

    st.subheader("Interview preparation")
    st.markdown(
        """
        - **US tax:** Explain how you would verify the tax year, source documents,
          filing status, and authority before preparing a workpaper.
        - **Canadian tax:** Describe how you would distinguish federal and
          provincial/territorial considerations and document CRA sources.
        - **Accounting:** Explain what an arithmetic reconciliation PASS does—and
          does not—establish.
        """
    )
