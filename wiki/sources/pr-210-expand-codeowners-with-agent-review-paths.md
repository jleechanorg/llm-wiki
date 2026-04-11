---
title: "PR #210: Expand CODEOWNERS with agent review paths"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-210.md
sources: []
last_updated: 2026-03-16
---

## Summary
Expands CODEOWNERS to give jleechan2015 bot account auto-review authority on agent PRs.

### Added paths:
- src/ @jleechan2015
- launchd/ @jleechan2015
- roadmap/ @jleechan2015
- docs/ @jleechan2015
- skills/ @jleechan2015
- lib/ @jleechan2015
- * @jleechan2015 (catch-all at root)

Existing:
- scripts/ @jleechan2015
- .claude/ @jleechan2015

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **High Risk**
> High risk because `ao-backfill.sh` now performs automated `gh pr merge` actions; the new auto-merge

## Metadata
- **PR**: #210
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +91/-0 in 2 files
- **Labels**: none

## Connections
