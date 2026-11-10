# Architecture — Sovereign OS preview

## Application modules

```text
app.py
├── modules/dashboard.py
├── modules/accounting/ ── core/reconciliation.py
├── modules/us_tax/ and modules/canada_tax/
├── modules/learning/
├── modules/career/
├── modules/assistant/ ── optional HTTPS provider call
└── modules/automation/ ── optional read-only GitHub API call
```

The tax workpaper UI sums explicitly entered line items only. It has no embedded tax
rates, filing rules, or official forms logic. Career uploads and trackers are kept
in the active Streamlit session and are not written to a database.

## Trust boundaries and external services

- The Streamlit host receives ledger and resume uploads. Use synthetic or redacted data.
- The reconciler performs arithmetic checks against supplied values only.
- An AI prompt is sent externally only after an explicit submit and confirmation.
- GitHub Actions status is fetched through a read-only GitHub REST API request.
- No email sender, Gmail connector, database, payment, workflow dispatch, or automated
  external write is integrated.
- External providers control their own terms, retention, availability, and any fees.

## Reconciliation meaning

`PASS` means the calculated closing balance is within the configured tolerance of the expected closing balance, based on the rows and control values supplied.

It does not prove source authenticity, completeness, correct account classification, correct tax treatment, or absence of fraud.

## Tax interpretation boundary

Tax-year selection is required for workpapers, but selecting a year does not load or
assert that year's rules. Users must verify sources, jurisdiction, facts, and
calculations independently.
