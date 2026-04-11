---
title: "PR #206: [agento] feat: add skeptic agent as 7th merge gate condition (bd-qw6)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-206.md
sources: []
last_updated: 2026-03-26
---

## Summary
Adds an independent **Skeptic Agent** as the **7th merge gate condition** (bd-qw6).

### What changed

**packages/core/src/types.ts:**
- `skepticRequired?: boolean` — when true, skeptic verdict is required for merge
- `skepticBypassProjects?: string[]` — projects exempt from skeptic (for bootstrapping)
- `getSkepticVerdict?(pr)` on SCM interface — returns "PASS" | "FAIL" | "SKIPPED"

**packages/core/src/merge-gate.ts:**
- 7th check: "Skeptic approved" — blocks merge when skepticRequired=true and

## Metadata
- **PR**: #206
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +1044/-2 in 22 files
- **Labels**: none

## Connections
