---
title: "PR 7212 XP canonicalization review handoff"
type: source
tags: [project, memory-file]
date: 2026-06-02
source_file: raw/memory_backfill_2026_06_13/project_2026-06-02_pr7212_xp_canonicalization_review.md
---

## Summary

Fresh review of PR https://github.com/jleechanorg/worldarchitect.ai/pull/7212 at head found the core deterministic final-state validator direction sound, but not mergeable. Blockers: can preserve explicit while rewriting from the default 5e table, producing contradictory canonical XP fields for custom thresholds. accepts canonical/legacy alias conflicts and threshold/delta contradictions.

## Key Claims

- `game_state.py` can preserve explicit `total_cumulative_next_level_exp_required`
- `narrative_response_schema._validate_experience` accepts canonical/legacy alias conflicts
- The PR body still advertises God Mode / streaming / contract-hash runtime work that is not
- Evidence is stale versus current head and non-test `mvp_site/**` files changed.
- GitHub reports `mergeable=CONFLICTING`, `mergeStateStatus=DIRTY`; same-session check rollup

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[Green Gate]]
- [[beads]]
- [[canonicalization]]
- [[7-green]]
- [[CodeRabbit]]
