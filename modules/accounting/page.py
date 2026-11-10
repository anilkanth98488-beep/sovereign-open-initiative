"""Streamlit interface for ledger import, reconciliation, and reports."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import streamlit as st

from core.reconciliation import Sovereign167VReconciler
from modules.accounting.ledger_io import LedgerImportError, read_ledger
from modules.accounting.reports import (
    build_transaction_report,
    reconciliation_json,
    safe_csv,
)

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_LEDGER = ROOT / "sample_data" / "synthetic_ledger.csv"


def _fingerprint(
    ledger: pd.DataFrame, opening: str, expected: str, tolerance: str
) -> str:
    data = "\n".join((ledger.to_csv(index=False), opening, expected, tolerance))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _show_result(result: dict) -> None:
    status = result["status"]
    if status == "PASS":
        st.success(f"{status}: {result['details']}")
    elif status == "NOT TESTED":
        st.warning(f"{status}: {result['details']}")
    else:
        st.error(f"{status}: {result['details']}")

    if "total_records" not in result:
        return
    columns = st.columns(4)
    columns[0].metric("Transactions", result["total_records"])
    columns[1].metric("Credits", result["total_credits"])
    columns[2].metric("Debits", result["total_debits"])
    columns[3].metric("Net activity", result["net_activity"])
    if "calculated_closing" not in result:
        return

    balances = st.columns(3)
    balances[0].metric("Calculated closing", result["calculated_closing"])
    balances[1].metric("Difference vs expected", result["variance"])
    balances[2].metric("Tolerance", result["tolerance"])
    with st.expander("Full reconciliation result"):
        st.json(result)


def render() -> None:
    st.header("Accounting & Reconciliation")
    st.caption(
        "CSV and Excel (.xlsx) import · Decimal arithmetic · formula-safe report exports"
    )
    st.warning(
        "Use synthetic data only. Uploaded files are processed by this Streamlit session; "
        "do not upload confidential, client, taxpayer, payroll, or banking records."
    )
    source = st.radio(
        "Ledger source", ("Bundled sample", "Upload file"), horizontal=True
    )
    ledger: pd.DataFrame | None = None
    uploaded = None
    source_id = "sample"

    if source == "Bundled sample":
        try:
            ledger = pd.read_csv(SAMPLE_LEDGER)
        except (OSError, UnicodeDecodeError, pd.errors.ParserError) as exc:
            st.error(f"Could not load the bundled synthetic ledger: {exc}")
    else:
        uploaded = st.file_uploader(
            "Upload a synthetic ledger",
            type=["csv", "xlsx"],
            help="Maximum 25 MB. Excel workbooks use their first worksheet.",
        )
        if uploaded is not None:
            source_id = hashlib.sha256(uploaded.getvalue()).hexdigest()
            try:
                ledger = read_ledger(uploaded.name, uploaded.getvalue())
            except LedgerImportError as exc:
                st.error(str(exc))

    if ledger is None:
        if source == "Upload file" and uploaded is None:
            st.info("Upload a CSV or XLSX file to preview it.")
        return

    st.subheader("Ledger preview")
    st.caption(f"{len(ledger):,} transactions · {len(ledger.columns):,} columns")
    st.dataframe(ledger, hide_index=True)

    with st.form("accounting_reconciliation"):
        controls = st.columns(3)
        opening = controls[0].text_input("Opening balance", value="1000.00")
        expected = controls[1].text_input("Expected closing balance", value="1450.00")
        tolerance = controls[2].text_input("Tolerance", value="0.01")
        submitted = st.form_submit_button("Reconcile ledger", type="primary")

    fingerprint = _fingerprint(ledger, opening, expected, tolerance)
    result_key = f"accounting_result_{source_id}"
    fingerprint_key = f"accounting_fingerprint_{source_id}"
    if submitted:
        result = Sovereign167VReconciler(
            ledger,
            opening_balance=opening,
            expected_closing_balance=expected,
            tolerance=tolerance,
        ).execute_reconciliation()
        st.session_state[result_key] = result
        st.session_state[fingerprint_key] = fingerprint
        st.session_state["recent_activities"].insert(
            0, f"Reconciled {source_id[:12]} · {result['status']}"
        )

    if st.session_state.get(fingerprint_key) != fingerprint:
        missing = [
            column
            for column in Sovereign167VReconciler.REQUIRED_COLUMNS
            if column not in ledger.columns
        ]
        if missing:
            st.warning(f"Required columns missing: {', '.join(missing)}.")
        st.info("Enter the control balances and run a reconciliation.")
        return

    result = st.session_state[result_key]
    _show_result(result)
    if result.get("status") not in {"PASS", "FAIL"}:
        return

    try:
        report = build_transaction_report(ledger, result)
    except (ValueError, KeyError) as exc:
        st.error(f"Could not build the transaction report: {exc}")
        return
    st.subheader("Transaction differences")
    st.caption(
        "The final transaction row shows the closing-balance variance; individual source "
        "transactions are not independently verified."
    )
    st.dataframe(report, hide_index=True)
    st.download_button(
        "Download reconciliation CSV",
        data=safe_csv(report),
        file_name="reconciliation-transactions.csv",
        mime="text/csv",
    )
    st.download_button(
        "Download reconciliation JSON",
        data=reconciliation_json(result),
        file_name="reconciliation-result.json",
        mime="application/json",
    )
