---
title: "Archive not delete + verify content before pruning by usage stats"
type: source
tags: [claude-code, skills, methodology, harness-hygiene]
date: 2026-07-07
source_file: raw/feedback_2026-07-07_archive_not_delete_and_verify_before_prune.md
---

## Summary

Two durable rules from executing a skill-cleanup recommendation: (1) always archive (move to a dated `_archive/_removed-YYYY-MM-DD/` directory) rather than delete anything based on a usage/redundancy claim, for full reversibility; (2) always diff the actual content before pruning based on a usage-stat claim alone — a 2026-07-07 audit's initial "archive all 16 zero-usage tessl__X skills as duplicates" recommendation turned out wrong for 10 of 16 pairs, which had genuine methodology differences a usage stat couldn't reveal.

## Key Claims

- Zero-usage-in-a-window is a selection-bias signal (which of two offered options the model happens to prefer), not a quality signal.
- Blanket-archiving based on usage stats risks silently deleting genuinely better/different logic that just wasn't being picked.
- The correct disposition for genuinely-differing "duplicate" pairs is usually back-port-then-archive, not keep-or-delete.

## Connections

- [[tool-use-grep-adjacency-false-negative]] — a same-day, same-pattern mistake (trusting a usage/measurement claim without verifying it) that nearly cost two actively-used MCP servers
- [[evidence-review-triple-duplicate-dead-code]] — a related same-day finding about silently-stale duplicate files
