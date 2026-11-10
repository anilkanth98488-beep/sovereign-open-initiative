# Sovereign OS — Sovereign Open Initiative

> **Open technology. Accessible knowledge. Community development.**

Sovereign OS is a modular Streamlit workspace for synthetic-data accounting
demonstrations, tax-learning workpapers, professional learning and career planning,
plus optional AI and GitHub integrations.

**Release:** `v0.1-preview`  
**Founder attribution:** Deva Anil Kanth  
**License:** Apache License 2.0

## What this preview provides

- A dashboard with local health indicators, module status, recent session activity,
  and quick navigation.
- CSV and XLSX ledger import, duplicate-header checks, deterministic Decimal
  reconciliation, transaction previews, and CSV/JSON result downloads.
- US and Canadian tax-year-labeled educational workpapers that only total user-entered
  values and link to official source starting points.
- Original VITA/TCE, EA, CPA, US-tax, and Canada-tax learning prompts; quiz and
  session-only progress tracking.
- Session-only resume inventory, career skills, application tracking, and planning.
- An opt-in OpenAI-compatible assistant and read-only GitHub Actions run status.

This preview does **not** prepare or file tax returns, apply official tax-year rules,
provide tax/legal advice, certify compliance, extract PDF/OCR data, or validate the
truth and completeness of source documents.

## Public-benefit principles

1. **Free public access:** source code, documentation, sample data, and the basic demonstration are free.
2. **Optional support only:** donations, sponsorships, grants, and voluntary contributions are welcome but never required.
3. **Deterministic calculations:** monetary arithmetic in the reconciliation core uses `decimal.Decimal`.
4. **Privacy by design:** the public demo is intended for synthetic data only. Do not upload real taxpayer, client, banking, or confidential records.
5. **Human responsibility:** a reconciliation result only tests arithmetic against supplied values. It does not establish that source records are complete, genuine, correctly classified, or tax-compliant.
6. **Evidence-led claims:** accuracy, performance, security, and compliance claims must be supported by reproducible evidence.

## Installation and configuration

```bash
git clone https://github.com/anilkanth98488-beep/sovereign-open-initiative.git
cd sovereign-open-initiative
```

Use Python 3.10 or later. Create and activate a virtual environment:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
```

Install the application and test dependencies (Excel import uses `openpyxl`):

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` only if you want to configure optional integrations.
The application does not automatically load `.env`; export values in the shell or
configure deployment environment variables/Streamlit secrets. Never commit a real
API key or token. Available settings:

- `SOVEREIGN_GITHUB_REPOSITORY` — GitHub repository used as the default status target.
- `GITHUB_TOKEN` — optional GitHub API token, configured server-side.
- `SOVEREIGN_AI_API_KEY` — optional OpenAI-compatible provider key.
- `SOVEREIGN_AI_BASE_URL` and `SOVEREIGN_AI_MODEL` — optional provider endpoint/model.

The AI assistant sends a prompt to the selected external provider only after the user
submits it and confirms the disclosure. Provider fees, retention, and terms may apply.
Do not submit confidential information.

## Run the application

Start the Sovereign OS workspace from the repository root:

```bash
streamlit run app.py
```

Sidebar navigation opens Dashboard, Accounting, US & Canadian Tax, Learning & VITA,
Career, AI Assistant, and Automation. Accounting accepts CSV or first-sheet XLSX with
`Date` and `Amount` columns; positive amounts are credits and negative amounts are
debits. The bundled synthetic ledger reconciles from `1000.00` to `1450.00`.

Tax workpapers require explicit tax-year selection and do not infer rates or rules.
Career uploads and module progress are held in Streamlit session memory, not persisted
to a database. GitHub API reads and AI requests are optional external integrations.

Run the test suite:

```bash
python -m pytest -v
```

GitHub Actions runs the test suite on pushes and pull requests. The workspace is a
demonstration; use synthetic data only and never upload taxpayer, client, banking, or
other confidential records.

## Deployment

The app entry point is `app.py`. It can be evaluated on Streamlit Community Cloud or
a compatible deployment, subject to the host's current account, plan, resource, and
data-handling terms. Hosting is not guaranteed to be permanently free. Review
[`PRIVACY.md`](PRIVACY.md) before enabling external integrations.

## Module layout

```text
app.py
core/                     Shared reconciliation and configuration
modules/accounting/       CSV/XLSX ledger import and reconciliation reports
modules/us_tax/           US tax workpaper catalog and source links
modules/canada_tax/       Canadian tax workpaper catalog and source links
modules/learning/         Learning tracks, practice, and progress
modules/career/           Resume, skills, application, and career tools
modules/assistant/        Optional OpenAI-compatible AI integration
modules/automation/       Read-only GitHub Actions integration
tests/                    Unit and application tests
```

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
