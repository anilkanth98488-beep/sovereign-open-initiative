# Project Inventory

This is an inventory of seven related repositories based on supplied ZIP/source reviews. It is not a claim that their code is currently integrated into this central repository. Each project's current GitHub branch may have changed since the supplied archive was created.

| Repository | Observed role in supplied source | v0.1 treatment |
|---|---|---|
| `sovereign-ai` | Streamlit workspace, local task/data utilities, optional external AI gateway | Isolated; do not connect to real client data |
| `Sovereign-2026` | Streamlit dashboard and assorted automation scripts | Security remediation required before reuse; historical archive contained exposed credentials |
| `sovereign-tax-pipeline` | Demonstration tax extraction script with hardcoded synthetic values | Research/demo only; no functioning PDF or K-1 extraction verified |
| `sovereign-tax-systems` | Static HTML marketing/architecture page | Documentation source only; marketing claims need evidence |
| `sovereign-os` | Streamlit interface with response templates and PDF upload UI | UI prototype; PDF extraction not implemented in supplied source |
| `automated-compliance-engine` | Python legal-notice payload and dispatch demonstration | No real email dispatch or regulatory validation verified |
| `conscious-wealth-engine` | Small Next.js landing-page prototype | Incomplete prototype; tax/astrology/report features not implemented in supplied ZIP |

## Integration policy

Reuse code only after checking its current source, license compatibility, dependencies, secret history, privacy implications, tests, and provenance. Do not copy old credentials, customer data, unverified claims, or unsafe automation into this repository.

The central v0.1 app currently uses only `core/reconciliation.py`.
