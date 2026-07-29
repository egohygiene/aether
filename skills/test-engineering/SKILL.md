---
name: test-engineering
description: Design, implement, review, or repair deterministic automated tests across unit, component, integration, end-to-end, contract, snapshot, golden, accessibility, and regression layers. Use for test coverage gaps, flaky tests, regression protection, test architecture, fixtures, fakes, mocks, CI test failures, or validation strategy.
---

# Test Engineering

## Model the risk

Identify the behavior or contract at risk, failure impact, boundary under test, existing coverage, and evidence that confidence is insufficient. Read repository conventions and any applicable strategy such as `../../../.github/specs/testing-strategy.spec.md`.

## Choose the test layer

Use the lowest layer that provides sufficient confidence:

- unit tests for pure logic and invariants
- component or widget tests for isolated UI behavior
- contract tests for interface compatibility
- integration tests for real boundary interactions
- end-to-end tests for a small set of critical user journeys
- snapshot or golden tests for intentional stable presentation

Avoid duplicating the same assertion at every layer.

## Design deterministic tests

- Assert observable behavior and meaningful state transitions.
- Control time, randomness, locale, network, filesystem, environment, and concurrency.
- Prefer fakes for stable domain behavior; use mocks for interaction verification at true boundaries.
- Keep fixtures minimal, named, and representative.
- Test success, failure, boundary, and recovery behavior proportional to risk.
- Write a regression test that demonstrates the original defect when fixing a bug.

Never hide flakiness with arbitrary sleeps, broad retries, disabled tests, weak assertions, or over-mocking.

## Validate

Run the smallest focused command during iteration, then the relevant suite and repository-required checks. Inspect failures rather than updating expected output blindly. Confirm cleanup, isolation, parallel safety, platform assumptions, and CI compatibility.

Report behavior covered, layer selection, commands and results, remaining risk, and any production testability seam that requires separate authorization.
