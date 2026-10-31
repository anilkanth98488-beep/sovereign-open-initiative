import pandas as pd
import streamlit as st

from core.reconciliation import Sovereign167VReconciler

st.set_page_config(
    page_title="Sovereign Open Initiative | Public Preview",
    page_icon="🦅",
    layout="wide",
)

st.title("🦅 Sovereign Open Initiative")
st.caption("Public Preview v0.1 — Open technology. Accessible knowledge. Community development.")

st.warning(
    "Demonstration only. Use synthetic data. Do not upload real taxpayer, client, bank, "
    "payroll, identity, or confidential information. A PASS result is an arithmetic check, "
    "not an audit opinion, tax validation, or guarantee of source accuracy."
)

st.subheader("167V arithmetic ledger reconciliation")
st.write("Upload a CSV containing `Date` and `Amount` columns. Positive amounts are credits; negative amounts are debits.")

with st.expander("Control balances", expanded=True):
    col1, col2, col3 = st.columns(3)
    opening = col1.text_input("Opening balance", value="1000.00")
    expected = col2.text_input("Expected closing balance", value="1450.00")
    tolerance = col3.text_input("Tolerance", value="0.01")

uploaded = st.file_uploader("Choose a synthetic CSV ledger", type=["csv"])

if uploaded is not None:
    try:
        ledger = pd.read_csv(uploaded)
        st.subheader("Uploaded ledger preview")
        st.dataframe(ledger, use_container_width=True)
        if st.button("Run arithmetic reconciliation", type="primary"):
            result = Sovereign167VReconciler(
                ledger,
                opening_balance=opening,
                expected_closing_balance=expected,
                tolerance=tolerance,
            ).execute_reconciliation()
            status = result["status"]
            if status == "PASS":
                st.success(f"{status}: {result['details']}")
            elif status == "NOT TESTED":
                st.warning(f"{status}: {result['details']}")
            else:
                st.error(f"{status}: {result['details']}")
            st.json(result)
    except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as exc:
        st.error(f"Could not read this CSV: {exc}")
else:
    st.info("Try `sample_data/synthetic_ledger.csv` to test the demonstration.")
