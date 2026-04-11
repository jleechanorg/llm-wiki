---
title: "PR #199: [agento] fix(hooks): remove no-op pr-green-check.py hook"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-199.md
sources: []
last_updated: 2026-03-26
---

## Summary
The `pr-green-check.py` UserPromptSubmit hook was designed to rate-limit green-check polling, but it always exits 0 and outputs nothing to stdout. This means it never actually blocks any prompt — it just burns 2 REST API calls (PR state + CR review state) on every single prompt submission for branches matching its regex.

The branch-name PR regex (`[apr][a-z]-[0-9]{2,4}`) is also overly broad, matching branches like `fix/bd-soc-v2` as PR #2.

Related bead: bd-soc

## Metadata
- **PR**: #199
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +0/-225 in 1 files
- **Labels**: none

## Connections
