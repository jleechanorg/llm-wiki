---
title: "PR #765: Fix backend bugs from frontend team"
type: source
tags: []
date: 2025-11-20
source_file: raw/prs-/pr-765.md
sources: []
last_updated: 2025-11-20
---

## Summary
- Client conversationId validation matches backend (any non-empty trimmed string); follow-up task ai_universe-pd6 to decide long-term contract/enforcement.
- SecondOpinion secondary defaults restored to Grok+2 via shared selector; regression test enforces 3-model plan.
- Real-mode integration run performed (CI_SIMULATION=false) against local backend + real APIs.

## Metadata
- **PR**: #765
- **Merged**: 2025-11-20
- **Author**: jleechan2015
- **Stats**: +997/-108 in 13 files
- **Labels**: none

## Connections
