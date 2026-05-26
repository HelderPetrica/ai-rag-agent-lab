# Security

This repository is designed to be public.

## Safety Rules

- No real secrets.
- No `.env` file.
- No production credentials.
- No client data.
- No real legal documents.
- No proprietary prompts.
- No internal endpoints.
- No production billing, tenant or commercial rules.
- No private logs.
- No copied code from private repositories.

## Environment Variables

Only `.env.example` is committed. It contains placeholders and safe defaults. If provider integrations are added later, real keys must stay in local environment variables or a secret manager.

## Before Publishing

Run these checks before pushing:

```bash
pytest
git status --short
git ls-files | grep -E "\\.env$|credentials|secret|token|private|client"
```

On Windows PowerShell:

```powershell
pytest
git status --short
git ls-files | Select-String -Pattern "\.env$|credentials|secret|token|private|client"
```

Any match must be reviewed before publication.

