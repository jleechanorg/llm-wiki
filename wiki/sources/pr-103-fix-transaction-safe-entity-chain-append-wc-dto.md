---
title: "PR #103: fix: transaction-safe entity_chain append (WC-dto)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-103.md
sources: []
last_updated: 2026-03-26
---

## Summary
Concurrent append operations in `packages/backend/src/storage/entity_chain.ts` have a race condition: `block_count` and `prev_hash` are computed from the in-memory `this.blocks` array **outside** the SQLite transaction. If an external writer (another chain instance or process) inserts blocks between the read and the transaction commit, the append produces a duplicate `block_id` (UNIQUE constraint violation) or an incorrect `prev_hash` (hash-chain fork).

## Metadata
- **PR**: #103
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +232/-16 in 2 files
- **Labels**: none

## Connections
