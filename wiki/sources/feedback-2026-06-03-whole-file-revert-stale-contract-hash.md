---
title: "Feedback 2026-06-03 Whole File Revert Stale Contract Hash"
type: source
tags: [feedback, project, worldarchitect-ai, memory-file]
date: 2026-06-03
source_file: raw/memory_backfill_2026_06_13/feedback_2026-06-03_whole_file_revert_stale_contract_hash.md
---

## Summary

PR #7225 review fixes whole-file reverted to main via , but still recorded the PR's stale sha256 a phantom version bump (1.2.29 while main is 1.2.28). The self-hosted CI job (runs ) failed: only compares (not version) — so restoring the hash alone makes CI pass; the version bump in the error text is cosmetic. But for a file reverted to main, restore the (version 1.2.28 + main's sha256) so a reviewer doesn't flag a version bump with no content change.

## Key Claims

- (See raw memory file for full content)

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
