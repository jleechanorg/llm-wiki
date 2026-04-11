---
title: "PR #8: Add prompt contract manifest, 9-layer assertions, and LLM output schema/tests"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldai_claw/pr-8.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Adds prompt contract manifest for system instruction prompt with SHA-256 tracking and versioning.
- Adds Jest assertions that system instruction still contains required 9-layer contract phrases and canonical field-name contract.
- Adds JSON schema for the LLM turn response envelope (strict top-level keys, banned legacy field prevention, mechanic/ui block shapes).
- Adds docs ↔ code prompt registration regression checks and keeps registry wiring in source.
- Adds prompt contract regression test

## Metadata
- **PR**: #8
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +394/-0 in 8 files
- **Labels**: none

## Connections
