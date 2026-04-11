---
title: "PR #214: [antig] fix: companion state mutations not idempotent on tick replay"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-214.md
sources: []
last_updated: 2026-04-04
---

## Summary
Tick replay could cause state divergence because updateCompanion and UPDATE sessions SET state ran unconditionally on every tick while action inserts use INSERT OR IGNORE.

## Metadata
- **PR**: #214
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +72/-34 in 7 files
- **Labels**: none

## Connections
