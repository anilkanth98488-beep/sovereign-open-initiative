"""Deterministic ledger arithmetic reconciliation for synthetic/demo data."""

from __future__ import annotations

import datetime as dt
from decimal import Decimal, InvalidOperation
from typing import Any

import pandas as pd


class Sovereign167VReconciler:
    """Compare ledger activity with supplied opening and expected closing balances.

    PASS is an arithmetic result only. It is not an audit opinion or tax validation.
    """

    REQUIRED_COLUMNS = ("Date", "Amount")

    def __init__(
        self,
        df_ledger: pd.DataFrame,
        opening_balance: Any = None,
        expected_closing_balance: Any = None,
        tolerance: Any = "0.01",
    ) -> None:
        self.raw_df = df_ledger.copy() if isinstance(df_ledger, pd.DataFrame) else pd.DataFrame()
        self.opening_balance = self._to_decimal(opening_balance)
        self.expected_closing_balance = self._to_decimal(expected_closing_balance)
        self.tolerance = self._to_decimal(tolerance)

    @staticmethod
    def _to_decimal(value: Any):
        if value is None:
            return None
        try:
            if pd.isna(value):
                return None
        except (TypeError, ValueError):
            return "INVALID"
        try:
            text = str(value).strip()
            if not text:
                return None
            text = text.replace("$", "").replace(",", "")
            if text.startswith("(") and text.endswith(")"):
                text = "-" + text[1:-1]
            number = Decimal(text)
            if not number.is_finite():
                return "INVALID"
            return number
        except (InvalidOperation, ValueError, TypeError):
            return "INVALID"

    @staticmethod
    def _money(value: Decimal) -> str:
        return f"{value:.2f}"

    def _build_result(self, status: str, details: str, **kwargs) -> dict:
        result = {
            "status": status,
            "details": details,
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "protocol": "167V-DETERMINISTIC-DECIMAL-v0.1",
        }
        result.update(kwargs)
        return result

    def execute_reconciliation(self) -> dict:
        missing = [col for col in self.REQUIRED_COLUMNS if col not in self.raw_df.columns]
        if missing:
            return self._build_result(
                "INPUT ERROR", f"Missing required column(s): {', '.join(missing)}."
            )
        if self.raw_df.empty:
            return self._build_result("INPUT ERROR", "Transaction ledger is empty.")

        if self.tolerance in (None, "INVALID") or not isinstance(self.tolerance, Decimal):
            return self._build_result("INPUT ERROR", "Tolerance must be a finite non-negative number.")
        if self.tolerance < 0:
            return self._build_result("INPUT ERROR", "Tolerance cannot be negative.")

        amounts: list[Decimal] = []
        for position, (_, row) in enumerate(self.raw_df.iterrows(), start=1):
            date_value = row["Date"]
            if pd.isna(date_value) or not str(date_value).strip():
                return self._build_result("INPUT ERROR", f"Missing date at row {position}.")
            try:
                parsed_date = pd.to_datetime(date_value, errors="raise")
                if pd.isna(parsed_date):
                    raise ValueError("empty date")
            except (ValueError, TypeError, OverflowError):
                return self._build_result("INPUT ERROR", f"Invalid date at row {position}: {date_value!r}.")

            amount = self._to_decimal(row["Amount"])
            if amount is None or amount == "INVALID":
                return self._build_result(
                    "INPUT ERROR",
                    f"Invalid numeric amount at row {position}: {row['Amount']!r}.",
                )
            amounts.append(amount)

        for label, value in (
            ("Opening balance", self.opening_balance),
            ("Expected closing balance", self.expected_closing_balance),
        ):
            if value == "INVALID":
                return self._build_result("INPUT ERROR", f"{label} is not a valid finite number.")

        credits = sum((amount for amount in amounts if amount > 0), Decimal("0"))
        debits = abs(sum((amount for amount in amounts if amount < 0), Decimal("0")))
        net_activity = credits - debits
        common = {
            "total_records": len(amounts),
            "total_credits": self._money(credits),
            "total_debits": self._money(debits),
            "net_activity": self._money(net_activity),
        }

        if self.opening_balance is None or self.expected_closing_balance is None:
            return self._build_result(
                "NOT TESTED",
                "Opening or expected closing balance was not supplied; balance verification was not performed.",
                **common,
            )

        calculated = self.opening_balance + net_activity
        variance = calculated - self.expected_closing_balance
        status = "PASS" if abs(variance) <= self.tolerance else "FAIL"
        if status == "PASS":
            details = "Arithmetic reconciliation passed within the configured tolerance."
        else:
            details = (
                f"Calculated closing balance ({self._money(calculated)}) differs from "
                f"expected closing balance ({self._money(self.expected_closing_balance)})."
            )

        return self._build_result(
            status,
            details,
            **common,
            opening_balance=self._money(self.opening_balance),
            calculated_closing=self._money(calculated),
            expected_closing=self._money(self.expected_closing_balance),
            variance=self._money(variance),
            tolerance=self._money(self.tolerance),
        )

    @staticmethod
    def sanitize_spreadsheet_text(value: Any) -> str:
        """Escape untrusted text that could be interpreted as a spreadsheet formula.

        Use only for untrusted text fields, not numeric cells.
        """
        text = "" if value is None else str(value)
        if text.lstrip().startswith(("=", "+", "-", "@")):
            return "'" + text
        return text
