---
title: "PR #283: [agento] fix(harness): Evidence Gate merged-PR bypass + DISMISSED CR stalling + media-check mandate"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-283.md
sources: []
last_updated: 2026-03-29
---

## Summary
Fixes three PR blocker failure patterns that have caused 9+ PRs to stall at various gates:

1. **Evidence Gate permanent failure on merged/closed PRs** — Evidence Gate CI checks now skip for merged/closed PRs (pre-merge gate has no function post-merge)
2. **DISMISSED CR review stalling `approved-and-green`** — lifecycle now checks CR's reviews[] directly when `reviewDecision` is null, so dismissed CR → fresh-review cycle works correctly
3. **Evidence Media check failures from placeholder text**

## Metadata
- **PR**: #283
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +115/-2 in 5 files
- **Labels**: none

## Connections
