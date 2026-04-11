---
title: "PR #423: [agento] fix(cli): remove duplicate timeout in doctor-script.test.ts (bd-doctest)"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-423.md
sources: []
last_updated: 2026-04-11
---

## Summary
- Removes duplicate `, 30_000` positional timeout from the first `it()` in `doctor-script.test.ts`
- Vitest 3 does not support the 4-argument overload `it(name, options, fn, timeout)` — the timeout was already set via `{ timeout: 30000 }` in the options object
- Bug introduced in commit `5eeb15c3` after PR #403 merged; tracked as bead `bd-doctest`

## Metadata
- **PR**: #423
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
