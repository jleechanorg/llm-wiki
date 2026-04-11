---
title: "PR #270: fix(bug-hunt): correct date filter for merged PRs"
type: source
tags: []
date: 2026-03-19
source_file: raw/prs-worldai_claw/pr-270.md
sources: []
last_updated: 2026-03-19
---

## Summary
The daily bug hunt was reporting 0 PRs because  doesn't work with 269	feat: Phase 2 — MCP mail + merge_gate reviewer APPROVED (orch-tlkk.2)	feat/reviewer-loop-phase2	OPEN	2026-03-18T15:49:33Z.

**Fix:** Fetch all merged PRs and filter with jq using ISO date comparison:



There are 10+ merged PRs in jleechanclaw alone from the last 2 days that should have been scanned.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Touches operational automation (`scripts/bug-hunt-daily.sh` + `launc

## Metadata
- **PR**: #270
- **Merged**: 2026-03-19
- **Author**: jleechan2015
- **Stats**: +677/-679 in 9 files
- **Labels**: none

## Connections
