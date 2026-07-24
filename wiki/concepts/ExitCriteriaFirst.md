---
title: "ExitCriteriaFirst"
type: concept
tags: [design-process, exit-criteria, definition-of-done, adversarial-review]
date: 2026-07-04
---

# ExitCriteriaFirst

Design principle: define **how you will know the project is truly done and working** before
writing any spec, design, or code — and make those criteria game-proof against the agent that
will implement them.

## The bar for each criterion

- **Binary** — pass/fail, no "mostly".
- **Executable** — a stated command or observable check.
- **Externally anchored** — verified at the layer users experience (system-of-record state:
  GitHub API, process table, kernel denial), never implementer-authored logs/telemetry.
- Implementer artifacts are corroborating, never sufficient; the verifier **reproduces** rather
  than inspects; satisfaction via mock/dry-run/pre-seeded state = FAIL; default verdict is FAIL.

## Why first, not last

Goodhart's law: once work starts, every proxy in the spec (tests pass, coverage %, "code
merged") gets optimized directly. Criteria written after the fact rationalize what was built.
The 2026-07-04 dark-factory case: a rigorous-looking draft DoD survived zero contact with three
hostile reviewers — ~20 loopholes and ~14 missing failure classes (agent-authored telemetry as
evidence, negative controls with no positive twin, replay-as-reproduction, conflated skeptics).
Canonical hardened charter: `dark-factory/docs/cutover-exit-criteria.md` (R1–R6 + X1–X10).

## Where it is enforced

- `/design` command + design-doc/design/spec-design-docs skills: Phase 0 writes exit criteria
  before any spec content, via superpowers brainstorming in batch-decision mode (all
  recommended decisions presented at once for one-pass review).
- superpowers brainstorming skill: exit-criteria exploration is a required area; the resulting
  no-code spec leads with an Exit Criteria section.
- Stage-1 adversarial review gate (three-doc rule): checks criteria are game-proof before
  design begins.

## Connections

- [[AdversarialEvaluation]] — hostile reviewers attack the criteria before work starts
- [[AdversarialTesting]] — fault-injection controls with pre-stated hypotheses
- Source: [Design exit-criteria-first wiring (2026-07-04)](../sources/feedback-2026-07-04-design-exit-criteria-first-wiring.md)
