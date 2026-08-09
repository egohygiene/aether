# Security Policy

## Reporting a vulnerability

Please report vulnerabilities privately to repository maintainers through GitHub Security Advisories or private maintainer contact channels. Do not open a public issue for undisclosed vulnerabilities.

## Scope and threat model notes

Aether ships instruction artifacts (`SKILL.md`, `AGENT.md`, templates, eval fixtures, staged provenance records) that can influence tool execution in downstream hosts.

Treat these as executable instruction resources:

- review external links and referenced scripts;
- apply least-privilege tool selection for agents;
- verify provenance before promoting staged content;
- never embed credentials/tokens/secrets in canonical or generated artifacts.

## Maintainer baseline checks

Before merging security-relevant changes:

```sh
./aether validate --format "text"
./aether validate --provenance --format "text"
./aether validate --links --format "text"
python3 catalog/validate_catalog.py
```

For installation/release surfaces, validate publishability without publishing:

```sh
gh skill publish "dist" --dry-run
```
