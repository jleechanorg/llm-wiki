---
title: "PR #255: [agento] fix: replace idx++ pattern with forEach in mergeGate tests"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-255.md
sources: []
last_updated: 2026-03-28
---

## Summary
Replace `let idx = 0; values[idx++]` pattern with `values.forEach(v => ...)` in two mergeGate test files to fix `no-useless-assignment` ESLint errors.

**Files**:
- `packages/cli/__tests__/commands/skeptic/mergeGate.test.ts`
- `packages/cli/__tests__/commands/skeptic/mergeGate.debug.test.ts`

**Change**: In `setupGhJson()`, replace sequential `mockGhJson.mockResolvedValueOnce(values[idx++] as any)` calls with `values.forEach(v => mockGhJson.mockResolvedValueOnce(v as any))`. Same behavior, elimi

## Metadata
- **PR**: #255
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +213/-13 in 5 files
- **Labels**: none

## Connections
