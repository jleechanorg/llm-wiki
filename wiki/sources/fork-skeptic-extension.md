---
title: "fork-skeptic-extension.ts"
type: source
tags: []
date: 2026-04-21
source_file: packages/core/src/fork-skeptic-extension.ts
---

## Summary
Skeptic extension module for the AO fork — extracted from lifecycle-manager.ts to keep that module thin. Implements the skeptic-review reaction case via `runSkepticReviewReaction()`, which calls `runSkepticReview()` from skeptic-reviewer.js. Supports codex, claude, and gemini models; SKIPPED verdicts are treated as non-success (not PASS) so the orchestrator can surface and retry.

## Key Claims
- Only PASS verdicts are treated as success; SKIPPED (all-infra-fail) must not be treated as PASS
- The completion trigger (fires on pr_open transition) lives in lifecycle-manager.ts because it requires access to transition variables (oldStatus, newStatus) not easily passed through a hook API
- Takes only primitive-compatible types so lifecycle-manager doesn't need to pass closure dependencies through the interface

## Key Quotes
> "SKIPPED (all-infra-fail) must not be treated as PASS — it is a non-success state that the orchestrator should surface and retry. Only PASS is success."

## Connections
- [[lifecycle-manager]] — imports and delegates to this module
- [[skeptic-reviewer]] — runSkepticReview is imported from this module
- [[fork-skeptic-extension]] — this module's own concept page
