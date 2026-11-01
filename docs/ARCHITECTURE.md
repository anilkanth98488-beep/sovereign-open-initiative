# Architecture — v0.1-preview

## Current execution path

```text
Visitor
  |
  v
Streamlit app.py
  |
  v
CSV upload (synthetic data recommended)
  |
  v
core/reconciliation.py
  |
  v
PASS / FAIL / NOT TESTED / INPUT ERROR
```

## Trust boundaries

- The Streamlit host receives the uploaded file. Do not treat the public demo as local-only.
- The reconciler performs arithmetic checks against values supplied by the user.
- No AI provider, email sender, Gmail connector, database, or payment integration is active in v0.1.
- The seven related repositories are inventoried as separate projects; they are not imported or technically integrated by this release.

## Reconciliation meaning

`PASS` means the calculated closing balance is within the configured tolerance of the expected closing balance, based on the rows and control values supplied.

It does not prove source authenticity, completeness, correct account classification, correct tax treatment, or absence of fraud.

## Future integration gates

Any module integration must pass code review, dependency review, unit tests, privacy/data-flow review, secret scanning, and explicit human approval for external side effects.
