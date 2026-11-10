import pandas as pd

from core.reconciliation import Sovereign167VReconciler


def ledger(rows):
    return pd.DataFrame(rows, columns=["Date", "Amount"])


def test_pass():
    df = ledger([("2026-11-01", "500.00"), ("2026-11-02", "-50.00")])
    result = Sovereign167VReconciler(df, "1000.00", "1450.00").execute_reconciliation()
    assert result["status"] == "PASS"
    assert result["variance"] == "0.00"


def test_fail():
    df = ledger([("2026-11-01", "100.00")])
    result = Sovereign167VReconciler(df, "500.00", "700.00").execute_reconciliation()
    assert result["status"] == "FAIL"
    assert result["variance"] == "-100.00"


def test_not_tested_when_control_missing():
    df = ledger([("2026-11-01", "25.00")])
    result = Sovereign167VReconciler(df, opening_balance="100.00").execute_reconciliation()
    assert result["status"] == "NOT TESTED"


def test_invalid_amount():
    df = ledger([("2026-11-01", "not-a-number")])
    assert Sovereign167VReconciler(df, "0", "0").execute_reconciliation()["status"] == "INPUT ERROR"


def test_non_finite_amount_rejected():
    df = ledger([("2026-11-01", "NaN")])
    assert Sovereign167VReconciler(df, "0", "0").execute_reconciliation()["status"] == "INPUT ERROR"


def test_extreme_decimal_exponent_rejected_without_formatting_huge_value():
    df = ledger([("2026-11-01", "1e1000000")])
    assert Sovereign167VReconciler(df, "0", "0").execute_reconciliation()["status"] == "INPUT ERROR"


def test_invalid_date_rejected():
    df = ledger([("not-a-date", "10.00")])
    assert Sovereign167VReconciler(df, "0", "10").execute_reconciliation()["status"] == "INPUT ERROR"


def test_missing_column_rejected():
    df = pd.DataFrame({"Date": ["2026-11-01"], "Debit": ["10.00"]})
    assert Sovereign167VReconciler(df, "0", "10").execute_reconciliation()["status"] == "INPUT ERROR"


def test_duplicate_columns_rejected():
    df = pd.DataFrame(
        [["2026-11-01", "2026-11-02", "10.00"]],
        columns=["Date", "Date", "Amount"],
    )
    result = Sovereign167VReconciler(df, "0", "10").execute_reconciliation()
    assert result["status"] == "INPUT ERROR"
    assert result["details"] == "Duplicate column name(s): Date."


def test_negative_tolerance_rejected():
    df = ledger([("2026-11-01", "10.00")])
    assert Sovereign167VReconciler(df, "0", "10", tolerance="-0.01").execute_reconciliation()["status"] == "INPUT ERROR"


def test_parenthesized_negative_amount():
    df = ledger([("2026-11-01", "(12.50)")])
    result = Sovereign167VReconciler(df, "100.00", "87.50").execute_reconciliation()
    assert result["status"] == "PASS"


def test_formula_injection_sanitization():
    assert Sovereign167VReconciler.sanitize_spreadsheet_text("=SUM(A1:A10)") == "'=SUM(A1:A10)"
    assert Sovereign167VReconciler.sanitize_spreadsheet_text("  @SUM(A1)") == "'  @SUM(A1)"
    assert Sovereign167VReconciler.sanitize_spreadsheet_text("normal text") == "normal text"
