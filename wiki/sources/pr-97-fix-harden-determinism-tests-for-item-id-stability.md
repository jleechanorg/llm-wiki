---
title: "PR #97: fix: harden determinism tests for item ID stability (wc-qh7)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-97.md
sources: []
last_updated: 2026-03-26
---

## Summary
Bug wc-qh7: `Date.now()` was previously used as a fallback in `seedForIds` when no `tickSeed` was provided in `resolveCompanionAction`. This made item IDs non-deterministic — the same simulation run could produce different loot item IDs. The code fix (replacing `Date.now()` with `effectiveSeed = tickSeed ?? 0`) was already landed on `main` as part of the WC-a22 determinism work, but the test coverage had a gap: one test was flaky and there was no explicit format assertion.

## Metadata
- **PR**: #97
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +34/-3 in 1 files
- **Labels**: none

## Connections
