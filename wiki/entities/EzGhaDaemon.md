---
title: "Ez Gha Daemon"
type: entity
tags: []
date: 2026-07-06
sources:
  - "[[learnings-2026-07]]"
---

## Summary
Ez Gha Daemon — referenced in the 2026-07-06 /learn recap on ez-gha-actions fleet rollout failures. See [[learnings-2026-07]] for full context.

## Connections
- [[learnings-2026-07]] — primary source
- [Doc-stated safety policy must be code-enforced (2026-07-17)](../sources/feedback-2026-07-17-doc-stated-policy-must-be-code-enforced.md) — the ezgha-watchdog SKILL.md's "fail-closed" restart policy wasn't actually enforced by the live script until this fix (`EZGHA_WATCHDOG_ALLOW_RESTART` gate)
