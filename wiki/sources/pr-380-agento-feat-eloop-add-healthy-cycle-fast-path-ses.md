---
title: "PR #380: [agento] feat(eloop): add healthy-cycle fast path + session budget (bd-l5ko)"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldai_claw/pr-380.md
sources: []
last_updated: 2026-04-05
---

## Summary
Eloop generates ~150K+ tokens over long sessions by running full observation phase even when nothing changed. This PR adds a healthy-cycle fast path and session budget guard to `generateEvolveLoopSection()`.

## Metadata
- **PR**: #380
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +83/-1 in 2 files
- **Labels**: none

## Connections
