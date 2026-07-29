# Custom Patterns Reference

Detailed reference for defining custom secret scanning patterns using regular expressions at the repository, organization, and enterprise level.

## Overview

Custom patterns extend secret scanning to detect organization-specific secrets not covered by default patterns. They are defined as regular expressions and can optionally enforce push protection.

## Pattern Definition

### Required Fields

| Field | Description |
| --- | --- |
| **Pattern name** | Human-readable name for the pattern |
| **Secret format** | Regular expression matching the secret |

### Optional Fields (via "More options")

| Field | Description |
| --- | --- |
| **Before secret** | Regex for content that must appear before the secret |
| **After secret** | Regex for content that must appear after the secret |
| **Additional match requirements** | Extra constraints on the match |
| **Sample test string** | Example string to validate the regex |

### Regex Syntax

Custom patterns use standard regular expressions. Common patterns:

```
# API key with prefix
MYAPP_[A-Za-z0-9]{32}

# Connection string
Server=[\w.]+;Database=\w+;User Id=\w+;Password=[^;]+

# Internal token format
myorg-token-[a-f0-9]{64}

# JWT-like pattern
eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+
```

Use filter patterns similar to GitHub Actions workflow syntax for glob-style matching in before/after fields.

## Defining Patterns by Scope

### Repository Level

1. Repository Settings → Advanced Security
1. Under "Secret Protection" → Custom patterns → **New pattern**
1. Enter pattern name, regex, and optional fields
1. **Save and dry run** to test
1. Review results (up to 1,000 matches)
1. **Publish pattern** when satisfied
1. Optionally enable push protection

**Prerequisite:** Secret Protection must be enabled on the repository.

### Organization Level

1. Organization Settings → Advanced Security → Global settings
1. Under "Custom patterns" → **New pattern**
1. Enter pattern details
1. **Save and dry run** — select repositories for testing:
   - All repositories in the organization, or
   - Up to 10 selected repositories
1. **Publish pattern** when satisfied
1. Optionally enable push protection

**Notes:**

- Push protection for org-level custom patterns only applies to repos with push protection enabled
- Organization owners and repo admins receive alerts

### Enterprise Level

1. Enterprise settings → Policies → Advanced Security → Security features
1. Under "Secret scanning custom patterns" → **New pattern**
1. Enter pattern details
1. **Save and dry run** — select up to 10 repositories
1. **Publish pattern** when satisfied
1. Optionally enable push protection

**Notes:**

- Only the pattern creator can edit or dry-run enterprise-level patterns
- Dry runs require admin access to the selected repositories
- Push protection requires enterprise-level secret scanning push protection to be enabled

## Dry Run Process

Dry runs test patterns against repository content without creating alerts.

1. Click **Save and dry run** after defining the pattern
1. Select target repositories (org/enterprise level)
1. Click **Run**
1. Review up to 1,000 sample results
1. Identify false positives
1. Edit pattern and re-run if needed
1. **Publish pattern** only when false positive rate is acceptable

> Dry runs are essential — always test before publishing to avoid alert noise.

## Managing Published Patterns

### Editing Patterns

After publishing, patterns can be edited:

1. Navigate to the custom pattern
1. Modify the regex or optional fields
1. Save and dry run to validate changes
1. Publish the updated pattern

### Enabling Push Protection

Push protection can only be enabled after a pattern is published:

1. Navigate to the published pattern
1. Click **Enable** next to push protection

**Caution:** Enabling push protection for commonly found patterns can disrupt contributor workflows.

### Disabling or Deleting Patterns

- Disable: stops new alert generation but retains existing alerts
- Delete: removes the pattern and stops all scanning for it

## Copilot-Assisted Pattern Generation

Use Copilot secret scanning to generate regex automatically:

1. Navigate to custom pattern creation
1. Select "Generate with Copilot" (if available)
1. Provide a text description of the secret type (e.g., "internal API key starting with MYORG_ followed by 40 hex characters")
1. Optionally provide example strings that should match
1. Copilot generates a regex pattern
1. Review and refine the generated regex
1. Test with dry run before publishing

## Pattern Inheritance

| Scope | Applies To |
| --- | --- |
| Repository | That repository only |
| Organization | All repos in the org with secret scanning enabled |
| Enterprise | All repos across all orgs with secret scanning enabled |

Organization and enterprise patterns automatically apply to new repositories when secret scanning is enabled.

## Best Practices

1. **Always dry run** before publishing — review for false positives
1. **Start specific** — narrow regexes reduce false positives
1. **Use before/after context** — adds precision without overly complex regex
1. **Test with real examples** — include sample strings that should and shouldn't match
1. **Document patterns** — name patterns clearly so teams understand what they detect
1. **Review periodically** — remove or update patterns that no longer apply
1. **Be cautious with push protection** — enable only for patterns with low false positive rates
1. **Consider Copilot** — let AI generate the initial regex, then refine manually
