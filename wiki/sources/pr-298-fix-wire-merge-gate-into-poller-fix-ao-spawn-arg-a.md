---
title: "PR #298: fix: wire merge_gate into poller, fix ao spawn arg, add auto-merge"
type: source
tags: []
date: 2026-03-20
source_file: raw/prs-worldai_claw/pr-298.md
sources: []
last_updated: 2026-03-20
---

## Summary
The PR poller (`ao-pr-poller.sh`) has three reliability issues preventing full autonomy:
1. The green check uses loose bash conditions that don't match `merge_gate.py`'s strict 6-condition check (e.g., treating any CR review as "approved")
2. `ao spawn` receives the project name as a positional arg, which ao interprets as "Issue identifier" — causing "Multiple projects configured" errors
3. When a PR *is* green, the poller spawns another agent instead of merging

## Metadata
- **PR**: #298
- **Merged**: 2026-03-20
- **Author**: jleechan2015
- **Stats**: +79/-66 in 3 files
- **Labels**: none

## Connections
