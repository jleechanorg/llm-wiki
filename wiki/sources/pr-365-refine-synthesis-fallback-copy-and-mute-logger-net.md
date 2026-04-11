---
title: "PR #365: Refine synthesis fallback copy and mute logger network calls in tests"
type: source
tags: [codex]
date: 2025-12-12
source_file: raw/prs-/pr-365.md
sources: []
last_updated: 2025-12-12
---

## Summary
- adjust the synthesis fallback messaging in MessageItem so the warning copy is unique while still surfacing the missing synthesis state
- skip backend logger network logging during tests to avoid MSW unhandled request noise while keeping sessionStorage logging

## Metadata
- **PR**: #365
- **Merged**: 2025-12-12
- **Author**: jleechan2015
- **Stats**: +6/-1 in 2 files
- **Labels**: codex

## Connections
