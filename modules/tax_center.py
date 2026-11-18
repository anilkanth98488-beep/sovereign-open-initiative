"""Tax-year-explicit, source-linked educational workpaper builder."""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal, InvalidOperation

import pandas as pd
import streamlit as st

from core.reconciliation import Sovereign167VReconciler
from modules.canada_tax.catalog import CANADA_REFERENCES, CANADA_TOPICS
from modules.us_tax.medical import SOURCE, calculate
from modules.us_tax.catalog import US_REFERENCES, US_TOPICS


def _parse_workpaper_amount(value: object) -> Decimal:
    text = str(value).strip().replace("$", "").replace(",", "")
    if len(text) > 64:
        raise InvalidOperation
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1]
    amount = Decimal(text)
    if (
        not amount.is_finite()
        or amount.adjusted() > 15
        or amount.as_tuple().exponent < -2
    ):
        raise InvalidOperation
    return amount


def render() -> None:
    st.header("US & Canadian Tax Centre")
    st.warning(
        "Educational workpapers only. Tax rules, thresholds, forms, and filing deadlines "
        "require a year-specific rule or manual review. Select a tax year and verify every "
        "item against current official sources or a qualified professional."
    )
    jurisdiction = st.radio(
        "Jurisdiction", ("United States", "Canada"), horizontal=True
    )
    if jurisdiction == "United States":
        topics, references = US_TOPICS, US_REFERENCES
        sub_jurisdiction_label = "State (optional)"
    else:
        topics, references = CANADA_TOPICS, CANADA_REFERENCES
        sub_jurisdiction_label = "Province or territory (optional)"
    sub_jurisdiction = st.text_input(
        sub_jurisdiction_label,
        help="For subnational workpapers, provide the specific state/province/territory. "
        "No subnational rules are automatically loaded.",
    )

    current_year = date.today().year
    years = ["Select a tax year"] + [
        str(year) for year in range(current_year - 6, current_year + 1)
    ]
    tax_year = st.selectbox("Tax year", years)
    if jurisdiction == "United States" and tax_year == "2025" and not sub_jurisdiction.strip():
        if st.checkbox("Use federal Schedule A medical expense rule"):
            st.subheader("Medical expense workpaper · 2025")
            st.caption("Synthetic cases only. Use positive or zero AGI. Review prior-year reimbursements separately.")
            st.markdown(f"[2025 Schedule A instructions]({SOURCE})")
            income = st.text_input("Form 1040 line 11b AGI (USD)")
            paid = st.text_input("Eligible medical expenses paid during 2025 (USD)")
            refunded = st.text_input("Same-year reimbursements for those expenses (USD)")
            checked = st.checkbox("I checked payment year, eligible persons and expenses, reimbursements, and duplicate deductions or tax-free payments.")
            if checked and all((income, paid, refunded)):
                try:
                    report = calculate(tax_year, income, paid, refunded)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.metric("Schedule A line 4 workpaper amount", report["line_4_excess_usd"])
                    st.json(report)
                    st.download_button("Download medical workpaper", json.dumps(report, indent=2),
                                       file_name="us-2025-medical.json", mime="application/json")
            return
    topic = st.selectbox("Workpaper area", list(topics))
    st.caption(topics[topic])

    st.markdown("**Official source starting points**")
    for label, url in references:
        st.markdown(f"- [{label}]({url})")

    st.info(
        "Calculation explanation: this page only sums the amounts you enter below. "
        "It does not apply statutory tax rates, deductions, credits, depreciation or "
        "CCA rules, elections, carryovers, state/provincial rules, or filing logic."
    )

    if tax_year == "Select a tax year":
        st.warning("Select the tax year this workpaper relates to; no year is assumed.")

    template = pd.DataFrame(
        [{"Line item": "", "Amount": "", "Source / note": ""}]
    )
    items = st.data_editor(
        template,
        key=f"tax_workpaper_{jurisdiction}_{tax_year}_{topic}",
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Line item": st.column_config.TextColumn("Line item"),
            "Amount": st.column_config.TextColumn("Amount"),
            "Source / note": st.column_config.TextColumn("Source / note"),
        },
    )

    line_items: list[dict[str, str]] = []
    amounts: list[Decimal] = []
    warnings: list[str] = []
    for position, row in items.iterrows():
        label = str(row.get("Line item", "")).strip()
        raw_amount = str(row.get("Amount", "")).strip()
        source_note = str(row.get("Source / note", "")).strip()
        if not label and not raw_amount and not source_note:
            continue
        if not label:
            warnings.append(f"Row {position + 1}: enter a line-item label.")
            continue
        if not raw_amount:
            warnings.append(f"Row {position + 1}: amount is blank; it is excluded.")
            continue
        try:
            amount = _parse_workpaper_amount(raw_amount)
        except (InvalidOperation, ValueError):
            warnings.append(f"Row {position + 1}: amount is not a valid finite number.")
            continue
        amounts.append(amount)
        line_items.append(
            {
                "line_item": Sovereign167VReconciler.sanitize_spreadsheet_text(label),
                "amount": f"{amount:.2f}",
                "source_note": Sovereign167VReconciler.sanitize_spreadsheet_text(
                    source_note
                ),
            }
        )

    for warning in warnings:
        st.warning(warning)

    if amounts and tax_year != "Select a tax year":
        total = sum(amounts, Decimal("0"))
        st.metric("Entered amount total (not a tax calculation)", f"{total:.2f}")
        report = {
            "jurisdiction": jurisdiction,
            "sub_jurisdiction": sub_jurisdiction.strip() or None,
            "tax_year": tax_year,
            "workpaper": topic,
            "calculation_explanation": (
                "Arithmetic sum of valid entered amounts only. No tax-year rules applied."
            ),
            "line_items": line_items,
            "entered_amount_total": f"{total:.2f}",
            "sources": [{"label": label, "url": url} for label, url in references],
            "warnings": warnings,
        }
        st.download_button(
            "Download workpaper (JSON)",
            data=json.dumps(report, indent=2),
            file_name=f"{jurisdiction.lower().replace(' ', '-')}-{tax_year}-workpaper.json",
            mime="application/json",
        )
    elif line_items:
        st.info("Select a tax year before viewing or exporting the workpaper total.")
