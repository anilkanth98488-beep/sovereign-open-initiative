# Contributing

Thank you for helping improve free and accessible open-source tools.

## Workflow

1. Fork the repository.
2. Create a focused branch, for example `feature/reconciliation-validation`.
3. Make the smallest clear change.
4. Add or update tests for behavior changes.
5. Run `python -m pytest -q`.
6. Open a pull request describing the change, risks, and test output.

## Engineering rules

- Use `decimal.Decimal` for monetary calculations.
- Reject malformed numeric inputs; never silently convert them to zero.
- Validate dates, required fields, finite numbers, and tolerances.
- Preserve source data and explain transformations.
- Escape untrusted text when exporting to spreadsheet-compatible formats; do not convert numeric values to text merely to sanitize them.
- Never add secrets or real personal/client data to commits, tests, screenshots, or issue reports.
- Do not add external integrations without documenting data flows and obtaining appropriate authorization.
- Avoid unsupported claims such as “IRS certified,” “audit-grade,” “100% accurate,” or “zero leakage.”

## License

By submitting a contribution, you agree that it is offered under the repository's Apache License 2.0, unless a separate written agreement says otherwise.
