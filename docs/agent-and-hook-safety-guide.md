# Agent and Hook Safety Guide

## Scope

Aether includes canonical agent source in `library/organization/agents/` and staged hook material in `.staging/hooks/`.

## Safety rules

- Treat agents/hooks as executable instruction resources.
- Use least-privilege tool declarations in agent frontmatter.
- Review shell/python hook scripts before promotion or reuse.
- Never add secrets, tokens, or private endpoints to agent/hook artifacts.
- Keep `.staging/` as non-canonical evidence unless promoted through governed review.

## Validation checks

```sh
python3 library/organization/agents/validate-agents.py
python3 library/organization/agents/build-projections.py --check
./aether validate --links --format "text"
```
