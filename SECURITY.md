# Security

This repository is designed to be public.

## Safety Rules

- No proprietary code.
- No private prompts.
- No real secrets.
- No `.env` file.
- No production credentials.
- No client data.
- No real legal documents.
- No internal endpoints.
- No commercial rules.
- No private logs.
- No copied code from private repositories.

## Environment Variables

Only `.env.example` is committed. It contains placeholders and safe defaults. If provider integrations are added later, real keys must stay in local environment variables or a secret manager.

## Sanitization Checks

The test suite includes a lightweight security smoke test for obvious secret patterns and accidental private product references. It is not a replacement for a full secret scanner, but it is a useful portfolio guardrail.

## Before Publishing

Run these checks before pushing:

```bash
pytest
python -m compileall app
git status --short
git ls-files | grep -E "\\.env$|credentials|secret|token|private|client"
```

On Windows PowerShell:

```powershell
pytest
python -m compileall app
git status --short
git ls-files | Select-String -Pattern "\.env$|credentials|secret|token|private|client"
```

Any match must be reviewed before publication.
