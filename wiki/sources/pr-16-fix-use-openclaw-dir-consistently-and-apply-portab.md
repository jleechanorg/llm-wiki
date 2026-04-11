---
title: "PR #16: fix: use openclaw dir consistently and apply portability"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-/pr-16.md
sources: []
last_updated: 2026-04-09
---

## Summary
Apply portability fixes: replace hardcoded /Users/jleechan with $HOME

Use .openclaw directory consistently:
- openclaw-upgrade-safe.sh: BASELINE_FILE uses ~/.openclaw
- gateway-preflight.sh: baseline file consistency  
- install-openclaw-launchd.sh: baseline path consistency

Based on jleechanclaw PR #538

Supersedes #15

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Touches deployment/upgrade and launchd automation; incorrect paths/labels or the new s

## Metadata
- **PR**: #16
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +91/-74 in 7 files
- **Labels**: none

## Connections
