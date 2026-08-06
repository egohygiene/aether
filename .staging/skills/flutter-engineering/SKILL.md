---
name: flutter-engineering
description: Design, implement, refactor, debug, or test Flutter and Dart application work using repository-aware architecture, state management, storage, routing, localization, design systems, notifications, AI-provider boundaries, code generation, and validation. Use for scoped Flutter feature and maintenance tasks.
---

# Flutter Engineering

## Resolve repository truth

1. Read `../../../.github/specs/flutter-engineer.spec.md` and relevant feature specifications when present.
1. Inspect the actual application path, `pubspec.yaml`, analyzer rules, formatter configuration, source patterns, tests, generators, and task automation.
1. Treat repository configuration as authoritative when generic guidance differs.
1. Confirm requested behavior, acceptance criteria, supported platforms, and privacy or offline constraints.

## Load only relevant references

- Architecture and feature boundaries: [architecture.md](references/architecture.md)
- Riverpod and state: [state-management.md](references/state-management.md)
- Offline-first storage and synchronization: [offline-first.md](references/offline-first.md)
- Routing and deep links: [routing.md](references/routing.md)
- Localization: [localization.md](references/localization.md)
- Design system and accessibility: [design-system.md](references/design-system.md)
- Notifications: [notifications.md](references/notifications.md)
- AI provider abstractions: [ai-providers.md](references/ai-providers.md)
- Testing: [testing.md](references/testing.md)

Do not load unrelated references solely because they exist.

## Implement a vertical slice

1. Place domain rules, data access, application state, and presentation in their established layers.
1. Reuse project abstractions before adding new ones.
1. Preserve explicit loading, data, empty, and error states.
1. Keep external services behind interfaces and inject dependencies through established mechanisms.
1. Route user-facing text through localization and use design-system tokens and components.
1. Include accessibility semantics, responsive behavior, privacy, and offline degradation when applicable.
1. Never hand-edit generated files; run the configured generator.

## Test and validate

Add the lowest appropriate tests for domain logic, repositories, providers, widgets, goldens, or user flows. Run dependency synchronization and generation only when required, then formatting, static analysis, focused tests, and repository-mandated checks. Use the task runner when it is the canonical interface.

Review the final diff for generated artifacts, dependency drift, localization coverage, state ownership, error visibility, accessibility, privacy, and unintended cross-feature coupling. Report changed behavior, checks and results, and any blocked validation.
