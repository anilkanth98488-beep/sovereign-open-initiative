"""Reconciliation report generation using exact decimal amounts."""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

import pandas as pd

from core.reconciliation import Sovereign167VReconciler


def _to_decimal(value: Any) -> Decimal:
    text = str(value).strip().replace("$", "").replace(",", "")
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1]
    return Decimal(text)


def build_transaction_report(
    ledger: pd.DataFrame, result: dict[str, Any]
) -> pd.DataFrame:
    """Return sanitized transaction rows with running balances and final variance."""
    if "total_records" not in result:
        raise ValueError("A valid reconciliation result is required for a transaction report.")

    opening = _to_decimal(result["opening_balance"])
    running = opening
    report_rows: list[dict[str, str]] = []
    for _, row in ledger.iterrows():
        amount = _to_decimal(row["Amount"])
        running += amount
        description = row.get("Description", "")
        safe_description = Sovereign167VReconciler.sanitize_spreadsheet_text(
            "" if pd.isna(description) else description
        )
        report_rows.append(
            {
                "Date": str(row["Date"]),
                "Description": safe_description,
                "Amount": f"{amount:.2f}",
                "Credit": f"{amount if amount > 0 else Decimal('0'):.2f}",
                "Debit": f"{abs(amount) if amount < 0 else Decimal('0'):.2f}",
                "Running balance": f"{running:.2f}",
                "Difference vs expected closing (final row)": "",
            }
        )

    report_rows[-1]["Difference vs expected closing (final row)"] = result["variance"]
    return pd.DataFrame(report_rows)


def reconciliation_json(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False)


def safe_csv(data: pd.DataFrame) -> str:
    """Serialize a report, neutralizing formula-like untrusted text fields."""
    safe = data.copy()
    for column in ("Date", "Description"):
        if column in safe.columns:
            safe[column] = safe[column].map(
                Sovereign167VReconciler.sanitize_spreadsheet_text
            )
    return safe.to_csv(index=False)
