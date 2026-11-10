from __future__ import annotations

from io import BytesIO
from pathlib import Path
from decimal import Decimal, InvalidOperation

import pandas as pd
import pytest
from openpyxl import Workbook

from core.config import Settings
from core.reconciliation import Sovereign167VReconciler
from modules.accounting.ledger_io import LedgerImportError, read_ledger
from modules.accounting.reports import build_transaction_report, safe_csv
from modules.assistant.client import AssistantError, ask_provider
from modules.automation.github import GitHubIntegrationError, fetch_workflow_runs
from modules.tax_center import _parse_workpaper_amount


def test_read_csv_and_reject_duplicate_headers():
    ledger = read_ledger(
        "ledger.csv",
        b"Date,Description,Amount\n2026-01-02,Service,10.00\n",
    )
    assert ledger.columns.tolist() == ["Date", "Description", "Amount"]
    with pytest.raises(LedgerImportError, match="Duplicate column"):
        read_ledger("duplicate.csv", b"Date,Date,Amount\n2026-01-01,other,1\n")


def test_read_xlsx_ledger():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Date", "Description", "Amount"])
    sheet.append(["2026-01-02", "Service", 10])
    contents = BytesIO()
    workbook.save(contents)

    ledger = read_ledger("ledger.xlsx", contents.getvalue())
    assert ledger.loc[0, "Description"] == "Service"
    assert ledger.loc[0, "Amount"] == 10


def test_xlsx_duplicate_headers_are_rejected():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Date", "Date", "Amount"])
    sheet.append(["2026-01-02", "other", 10])
    contents = BytesIO()
    workbook.save(contents)

    with pytest.raises(LedgerImportError, match="Duplicate column"):
        read_ledger("duplicate.xlsx", contents.getvalue())


def test_corrupt_xlsx_returns_readable_import_error():
    with pytest.raises(LedgerImportError, match="could not be read"):
        read_ledger("corrupt.xlsx", b"not an Excel workbook")


def test_transaction_report_uses_decimal_and_sanitizes_text():
    ledger = pd.DataFrame(
        [
            {"Date": "2026-01-01", "Description": "=FORMULA()", "Amount": "12.10"},
            {"Date": "2026-01-02", "Description": "Expense", "Amount": "-2.00"},
        ]
    )
    result = Sovereign167VReconciler(ledger, "100.00", "110.00").execute_reconciliation()
    assert result["status"] == "FAIL"
    report = build_transaction_report(ledger, result)
    assert report.loc[1, "Running balance"] == "110.10"
    assert report.loc[1, "Difference vs expected closing (final row)"] == "0.10"
    assert safe_csv(report).splitlines()[1].split(",")[1] == "'=FORMULA()"


def test_settings_read_secrets_and_environment_overrides(monkeypatch):
    monkeypatch.setenv("SOVEREIGN_AI_MODEL", "environment-model")
    settings = Settings.load(
        {
            "SOVEREIGN_AI_API_KEY": "test-key",
            "SOVEREIGN_AI_MODEL": "secret-model",
        }
    )
    assert settings.ai_api_key == "test-key"
    assert settings.ai_model == "environment-model"


def test_tax_workpaper_amount_is_cent_precise_and_bounded():
    assert _parse_workpaper_amount("($1,234.50)") == Decimal("-1234.50")
    with pytest.raises(InvalidOperation):
        _parse_workpaper_amount("0.001")
    with pytest.raises(InvalidOperation):
        _parse_workpaper_amount("1e1000")


def test_assistant_requires_https_and_valid_question():
    with pytest.raises(AssistantError, match="HTTPS"):
        ask_provider(
            "Explain depreciation",
            api_key="not-real",
            base_url="http://provider.invalid/v1",
            model="test-model",
        )
    with pytest.raises(AssistantError, match="Enter a question"):
        ask_provider(
            " ",
            api_key="not-real",
            base_url="https://provider.invalid/v1",
            model="test-model",
        )


def test_assistant_successful_response_without_exposing_credentials(monkeypatch):
    requested = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        @staticmethod
        def read():
            return b'{"choices":[{"message":{"content":"Use an official source."}}]}'

    def fake_urlopen(request, timeout):
        requested["request"] = request
        requested["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("modules.assistant.client.urlopen", fake_urlopen)
    result = ask_provider(
        "Explain bookkeeping",
        api_key="test-secret",
        base_url="https://provider.invalid/v1",
        model="test-model",
    )
    assert result == "Use an official source."
    assert requested["request"].get_header("Authorization") == "Bearer test-secret"
    assert "test-secret" not in result


def test_github_rejects_malformed_repository_before_network_call():
    with pytest.raises(GitHubIntegrationError, match="owner/name"):
        fetch_workflow_runs("https://example.invalid/repo")


def test_streamlit_navigation_pages_render():
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(
        Path(__file__).resolve().parents[1] / "app.py", default_timeout=20
    ).run()
    assert not app.exception
    for destination in (
        "Accounting",
        "US & Canadian Tax",
        "Learning & VITA",
        "Career",
        "AI Assistant",
        "Automation",
        "Dashboard",
    ):
        app.sidebar.radio[0].set_value(destination).run()
        assert not app.exception, (destination, app.exception)
        if destination == "Accounting":
            reconcile_button = next(
                button for button in app.button if button.label == "Reconcile ledger"
            )
            reconcile_button.click().run()
            assert not app.exception
            assert any("PASS" in item.value for item in app.success)


def test_dashboard_quick_navigation_updates_sidebar_without_state_error():
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(
        Path(__file__).resolve().parents[1] / "app.py", default_timeout=20
    ).run()
    quick_link = next(
        button for button in app.button if button.label == "Open Accounting"
    )
    app = quick_link.click().run()

    assert not app.exception
    assert app.sidebar.radio[0].value == "Accounting"
