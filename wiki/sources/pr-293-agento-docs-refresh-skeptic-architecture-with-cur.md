---
title: "PR #293: [agento] docs: refresh skeptic architecture with current component map"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-293.md
sources: []
last_updated: 2026-03-29
---

## Summary
Refreshed skeptic architecture documentation to reflect current implementation:
- Added skeptic-cron-local.ts, skeptic-reviewer.ts, fork-claim-verification.ts, llm-eval.ts as named components
- Documented skeptic-gate chain (fires on PR open/sync) and skeptic-cron chain (fires every 30min)
- Added self-referential skeptic PR guidance (expected to fail gates 1/3/5 during development)
- Added hook stdin testing step to Skeptic Change Verification checklist
- Added hook stdin piping red flag

## Metadata
- **PR**: #293
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +17/-6 in 1 files
- **Labels**: none

## Connections
