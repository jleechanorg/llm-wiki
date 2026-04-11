---
title: "PR #100: test: add IPFS-after-SQLite ordering regression tests (WC-3pg)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-100.md
sources: []
last_updated: 2026-03-26
---

## Summary
In commit 0405f55, the `append()` method in `entity_chain.ts` was fixed to move IPFS pinning after the SQLite row insert, preventing a race condition where IPFS failure could leave the chain in an inconsistent state. However, no regression tests were added to guard this ordering contract.

## Metadata
- **PR**: #100
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +285/-0 in 1 files
- **Labels**: none

## Connections
