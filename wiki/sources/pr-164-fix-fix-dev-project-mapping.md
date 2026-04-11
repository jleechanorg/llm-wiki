---
title: "PR #164: fix: fix dev project mapping"
type: source
tags: [codex]
date: 2025-10-04
source_file: raw/prs-/pr-164.md
sources: []
last_updated: 2025-10-04
---

## Summary
- update deployment scripts to always target the shared ai-universe-2025 project with extensive inline documentation
- ensure testing_llm config normalizes gcloud context, warns on mismatches, and consistently calls Cloud Run with explicit project flags
- remove all references to the deprecated ai-universe-dev-2025 identifier while keeping fallback URL logic intact

## Metadata
- **PR**: #164
- **Merged**: 2025-10-04
- **Author**: jleechan2015
- **Stats**: +154/-64 in 3 files
- **Labels**: codex

## Connections
