---
title: "PR #108: test: add TDD regression tests for SQLite FK enforcement (WC-myj)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-108.md
sources: []
last_updated: 2026-03-26
---

## Summary
The `entity_chain.ts` SQLite database has `PRAGMA foreign_keys = ON` in `initializeTables()` and a `FOREIGN KEY(entity_id) REFERENCES entity_chains(entity_id)` constraint on the `entity_blocks` table. However, there were no tests verifying that FK enforcement actually works — orphan inserts could silently succeed if someone removed the PRAGMA.

## Metadata
- **PR**: #108
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +92/-0 in 1 files
- **Labels**: none

## Connections
