# Sovereign Open Initiative

> **Open technology. Accessible knowledge. Community development.**

Sovereign Open Initiative is a free and open-source public-benefit project bringing together experiments in financial education, document workflows, deterministic ledger reconciliation, and compliance-support tooling.

**Release:** `v0.1-preview`  
**Founder attribution:** Deva Anil Kanth  
**License:** Apache License 2.0

## What v0.1 actually provides

- A Streamlit demonstration for CSV ledger arithmetic reconciliation.
- A deterministic four-state result: `PASS`, `FAIL`, `NOT TESTED`, or `INPUT ERROR`.
- Synthetic sample data and a small automated test suite.
- Documentation describing the seven related repositories and their current limitations.

This release does **not** provide tax-return preparation, IRS/CRA-approved calculations, certified compliance, OCR/PDF extraction, legal advice, audit assurance, or production-grade client-data processing.

## Public-benefit principles

1. **Free public access:** source code, documentation, sample data, and the basic demonstration are free.
2. **Optional support only:** donations, sponsorships, grants, and voluntary contributions are welcome but never required.
3. **Deterministic calculations:** monetary arithmetic in the reconciliation core uses `decimal.Decimal`.
4. **Privacy by design:** the public demo is intended for synthetic data only. Do not upload real taxpayer, client, banking, or confidential records.
5. **Human responsibility:** a reconciliation result only tests arithmetic against supplied values. It does not establish that source records are complete, genuine, correctly classified, or tax-compliant.
6. **Evidence-led claims:** accuracy, performance, security, and compliance claims must be supported by reproducible evidence.

## Quickstart

```bash
git clone https://github.com/anilkanth98488-beep/sovereign-open-initiative.git
cd sovereign-open-initiative
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
python -m pytest -q
```

Try `sample_data/synthetic_ledger.csv`. Its opening balance is `1000.00` and expected closing balance is `1450.00`.

## Deployment

The app entry point is `app.py`. It can be evaluated on Streamlit Community Cloud or a compatible Posit Connect deployment, subject to the host's current account, plan, resource, and data-handling terms. Hosting is not guaranteed to be permanently free. Configure no secrets for this v0.1 demo; never add secrets to source code or commit `.env` files.

## Repository map

See [docs/PROJECT_INVENTORY.md](docs/PROJECT_INVENTORY.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and [docs/ROADMAP.md](docs/ROADMAP.md).

## Status

This is an experimental public preview. Tests in this package are provided for local verification; do not describe them as passed until they have been run in your environment or CI.

## Governance

- [Security policy](SECURITY.md)
- [Privacy notice](PRIVACY.md)
- [Contributing guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Apache License 2.0](LICENSE)
