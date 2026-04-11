---
title: "PR #404: [agento] fix(backfill): make backfillAllPRs opt-out (default on)"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldai_claw/pr-404.md
sources: []
last_updated: 2026-04-07
---

## Summary
- Flip `backfillAllPRs` from opt-in to **opt-out** (default enabled). Any project value other than explicit `false` activates backfill + `runLocalSkepticCron`.
- Add warn-level `lifecycle.backfill.disabled_with_open_prs` observation when a project explicitly disables backfill but still has ≥1 non-draft open PR — silent misconfiguration becomes visible.
- Update the `backfillAllPRs` docstring in `types.ts` to describe the new default and warn signal.

## Metadata
- **PR**: #404
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +91/-9 in 6 files
- **Labels**: none

## Connections
