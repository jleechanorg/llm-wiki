---
title: "2026-06-13 Dark Factory Introduces Scope Drift"
type: source
tags: ["feedback", "worldarchitect", "dark-factory"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_dark_factory_introduces_scope_drift.md
---

## Summary
/f pipeline not only can

## Key Claims
- - The dark-factory pipeline's `goal` parameter is a feature spec, NOT a file-ownership constraint.
- - The `implement` and `fix` codergen nodes ask the LLM "implement this goal" — the LLM is free to touch any file it thinks is needed.
- - The LLM also sees the worktree's existing state and may include commits from prior rebase (which can pull in main commits if `origin/feat/levelup-v2-world-logic` is behind `main`).
- - The result: autonomous commits that look "themed" but violate the file-disjoint ownership rule from `docs/plans/2026-06-13-level-up-v2-immediate-commit.md:3, :48`.
- - ✅ In-scope: `apply_level_up atomic co-write reducer`, `route world_logic through v2 reducer; delete source=server 2nd writer`, `add is_review_open + close_review tests`, `migrate modal-lock tests to v2 contract`
- - ⚠️ Questionable: `bypass non-finish invariant when god-mode admin commit dispatched` (PR-6 scope?), `add behavioral holdout — immediate-commit regression suite` (PR-1 scope?), `guard P0 empty-sheet ordering (commit→reducer)` (PR-5/A scope?)

## Connections
- [[WorldarchitectAI]] — worldarchitect.ai project memory
- [[DarkFactory]] — dark-factory pipeline memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_dark_factory_introduces_scope_drift.md`
