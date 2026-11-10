"""CSV and Excel import helpers with early header validation."""

from __future__ import annotations

import csv
import io
from collections import Counter
from pathlib import Path
from zipfile import BadZipFile

import pandas as pd
from openpyxl.utils.exceptions import InvalidFileException


class LedgerImportError(ValueError):
    """Raised when a ledger upload cannot be safely read."""


MAX_LEDGER_UPLOAD_BYTES = 25 * 1024 * 1024
SUPPORTED_LEDGER_SUFFIXES = {".csv", ".xlsx"}


def _validate_headers(headers: tuple[object, ...] | list[object] | None) -> None:
    if not headers:
        raise LedgerImportError("The uploaded file has no header row.")
    normalized = [str(header).strip() if header is not None else "" for header in headers]
    if any(not header for header in normalized):
        raise LedgerImportError("The header row contains an empty column name.")
    duplicates = sorted(name for name, count in Counter(normalized).items() if count > 1)
    if duplicates:
        raise LedgerImportError(f"Duplicate column name(s): {', '.join(duplicates)}.")


def read_ledger(filename: str, content: bytes) -> pd.DataFrame:
    """Read the first worksheet or CSV table, rejecting ambiguous headers."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_LEDGER_SUFFIXES:
        raise LedgerImportError("Upload a .csv or .xlsx ledger file.")
    if not content:
        raise LedgerImportError("The uploaded file is empty.")
    if len(content) > MAX_LEDGER_UPLOAD_BYTES:
        raise LedgerImportError("The uploaded file exceeds the 25 MB size limit.")

    try:
        if suffix == ".csv":
            text = content.decode("utf-8-sig")
            header = next(csv.reader(io.StringIO(text, newline="")), None)
            _validate_headers(header)
            ledger = pd.read_csv(io.BytesIO(content))
        else:
            from openpyxl import load_workbook

            workbook = load_workbook(
                io.BytesIO(content), read_only=True, data_only=True
            )
            try:
                worksheet = workbook.active
                if worksheet is None:
                    raise LedgerImportError("The Excel workbook has no active worksheet.")
                header = next(
                    worksheet.iter_rows(min_row=1, max_row=1, values_only=True),
                    None,
                )
                _validate_headers(header)
            finally:
                workbook.close()
            ledger = pd.read_excel(io.BytesIO(content), sheet_name=0, engine="openpyxl")
    except LedgerImportError:
        raise
    except (
        UnicodeDecodeError,
        csv.Error,
        OSError,
        ValueError,
        KeyError,
        BadZipFile,
        InvalidFileException,
        pd.errors.ParserError,
    ) as exc:
        raise LedgerImportError(
            "The file could not be read as a valid CSV or Excel workbook."
        ) from exc

    if ledger.empty:
        raise LedgerImportError("The ledger contains a header but no transaction rows.")
    if ledger.columns.duplicated().any():
        raise LedgerImportError("The imported ledger contains duplicate column names.")
    return ledger
