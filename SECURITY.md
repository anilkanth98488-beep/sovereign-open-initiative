# Security Policy

## Supported release

Security reports are accepted for the current `v0.1-preview` source in this repository.

## Rules

- Never commit API keys, passwords, OAuth tokens, private keys, connection strings, or real customer data.
- Read secrets at runtime from environment variables (`os.getenv`) or the hosting provider's secret manager. Do not print secrets to logs.
- `.env` is for local development only and must remain untracked. `.env.example` must contain placeholders only.
- Public demos must use synthetic data. Do not upload real tax, bank, payroll, identity, or client documents.
- Do not claim that regular expressions or basic masking reliably anonymize personal data.
- Any future external AI integration must disclose the provider, data sent, purpose, retention considerations, and obtain appropriate authorization before transmission.
- Require human review before external communications or legal/compliance actions.

## Reporting

Please do not publish exploitable details or secrets in public issues. Use GitHub's private vulnerability reporting feature if enabled for the repository. If it is unavailable, contact the maintainer through a verified contact method published in the repository profile.

Do not rely on a guaranteed response or remediation deadline unless the maintainers have formally committed to one.

## If a secret is exposed

Revoke or rotate it at the issuing provider immediately. Removing it from the latest commit is not sufficient; review repository history, forks, logs, deployment settings, and any copies that may have been downloaded.
