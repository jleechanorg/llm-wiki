---
title: "Feedback 2026-05-30 Force Gate Breaks Predating Modal Test"
type: source
tags: [feedback, project, worldarchitect-ai, memory-file]
date: 2026-05-30
source_file: raw/memory_backfill_2026_06_13/feedback_2026-05-30_force_gate_breaks_predating_modal_test.md
---

## Summary

PR #7175 (Itachi L16 fix) approach-(a) added a force gate in (world_logic.py:2538-2559): when a canonical actionable pending transition arrives — even *first* via () — it force-writes AND to engage the modal so the finish turn routes through the exit-lock commit. The CI "Directory tests (core-mvp-1)" failure was (test_world_logic.py:8619), which predated the gate and asserted — i.e. the old narrower stale-scrub left the key absent.

## Key Claims

- (See raw memory file for full content)

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
