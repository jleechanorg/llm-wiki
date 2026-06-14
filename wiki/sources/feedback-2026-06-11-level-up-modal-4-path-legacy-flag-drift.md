---
title: "Feedback 2026 06 11 Level Up Modal 4 Path Legacy Flag Drift"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-11
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-11_level_up_modal_4_path_legacy_flag_drift.md
---

## Summary

**Rule:** When schema marks a legacy field `"deprecated": true` and introduces a canonical replacement (e.g. `level_up_session.status` replaces `custom_campaign_state.level_up_in_progress`), the migration is incomplete until EVERY backend reader of the legacy field is updated. The schema change is silent — LLM obeys the deprecation, but backend code that hasn't been touched still reads the now-stale legacy field.

## Original

# Canonical-field deprecation → audit all readers, not just the obvious one

**Rule:** When schema marks a legacy field `"deprecated": true` and introduces a canonical replacement (e.g. `level_up_session.status` replaces `custom_campaign_state.level_up_in_progress`), the migration is incomplete until EVERY backend reader of the legacy field is updated. The schema change is silent — LLM obeys the deprecation, but backend code that hasn't been touched still reads the now-stale legacy field.

## Specific lesson from level-up 2→3 routing (2026-06-11)

**Setup:** the modal lock routing at `mvp_site/agents.py:3329` was the most obvious reader of `custom_campaign_state.level_up_in_progress`. We fixed it. The fix worked for the routing case. But THREE OTHER code paths still read the legacy field:

1. `mvp_site/agents.py` modal lock routing — FIXED
2. `mvp_site/world_logic.py:2261+` modal state filter (preserves top-level level_up_session) — FIXED
3. `mvp_site/world_logic.py:3267` `_is_level_up_time_freeze_context` — NOT FIXED
4. `mvp_site/rewards_engine.py:1016` `block_unauthorized_level_mutations` — NOT FIXED

Result: routing worked, but freeze context returned False (causing 4× "non-finish turn advanced story/world state" failures), and mutation safety net rejected the level change (causing the main "got level 2" failure).

## Why this is hard to spot

- Routing is the highest-signal failure (modal doesn't lock at all, the symptoms are obvious in server.log:0 modal_lock events for the affected transition)
- Freeze and mutation failures produce DIFFERENT symptoms (turn counter advances; level reverts) that look like a different bug each
- An agent fixing only the routing bug will see "the test still fails, in a different way" and may attribute it to a new bug rather than recognizing it as a downstream reader of the same legacy field

## How to apply

Before declaring a canonical-field migration done, **grep the codebase for every reader of the legacy field**:

```bash
rg -n 'level_up_in_progress' mvp_site/ | grep -v test
rg -n 'level_up_pending' mvp_site/ | grep -v test
rg -n 'level_up_complete' mvp_site/ | grep -v test
rg -n 'level_up_stage' mvp_site/ | grep -v test
```

For each match, classify it as:
- (a) writer that should stop writing → update
- (b) reader that should switch to canonical → update
- (c) intentional compat reader (e.g. test cleanup) → leave with a comment

A migration is complete when (a) and (b) are zero. Test failures from canonical-field deprecations are almost always (b) lurking, not (a).

**Why:** 2 hours spent on a level-up routing fix that turned out to be 4 separate bugs in 4 separate code paths. The original 1→2 modal worked because the LLM was over-emitting (writing both fields); the 2→3 modal failed because the LLM correctly stopped writing the deprecated field. The failure mode flips silently when an LLM starts following the schema. Always grep for readers when promoting a canonical field.
