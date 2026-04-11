---
title: "PR #13: Reclaim agent names, retire old identities, and harden share wizard"
type: source
tags: []
date: 2025-11-07
source_file: raw/prs-/pr-13.md
sources: []
last_updated: 2025-11-07
---

## Summary
- add soft-delete tracking so reclaiming an agent name retires the prior identity (releases reservations, updates archives) and scope all discovery/routing queries to active agents only
- document the reclaimable-name flow, migrate DB uniqueness to active rows, and expand tests (including new reuse coverage)
- tighten the share wizard (saved-config fallback, stdout guards) plus polish CLI/test utilities so ruff/ty stay clean

## Metadata
- **PR**: #13
- **Merged**: 2025-11-07
- **Author**: jleechan2015
- **Stats**: +2084/-160 in 29 files
- **Labels**: none

## Connections
