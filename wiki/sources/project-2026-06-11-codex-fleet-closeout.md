---
title: "Project 2026 06 11 Codex Fleet Closeout"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-11
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_codex_fleet_closeout.md
---

## Summary

2026-06-11 close-out of the /f codex fleet (pipeline `pr_gates_no_holdout.dot`: /es + /er codex-first adversarial + /code_standards; authored after discovering `dark-factory-holdouts/holdouts/level-up-session/` is EMPTY — rev-krc9t):

- **Merge-ready (human-gated):** [#7441](https://github.com/jleechanorg/worldarchitect.ai/pull/7441) f417e482 (unlocks M2; evidence regenerated at head after codex flagged staleness; open call: 1-line `public_level_up_signal_contract` fix vs disclosed gap), [#7450]...

## Original

2026-06-11 close-out of the /f codex fleet (pipeline `pr_gates_no_holdout.dot`: /es + /er codex-first adversarial + /code_standards; authored after discovering `dark-factory-holdouts/holdouts/level-up-session/` is EMPTY — rev-krc9t):

- **Merge-ready (human-gated):** [#7441](https://github.com/jleechanorg/worldarchitect.ai/pull/7441) f417e482 (unlocks M2; evidence regenerated at head after codex flagged staleness; open call: 1-line `public_level_up_signal_contract` fix vs disclosed gap), [#7450](https://github.com/jleechanorg/worldarchitect.ai/pull/7450) 745e5e43, [#7451](https://github.com/jleechanorg/worldarchitect.ai/pull/7451) 3f88d7c8. Gate fails on 7450/7451 de-attributed via controls (class5 flake pre-existing; circular import repros on main — rev-dvr6h).
- **#7377 blocker (rev-lskmv P1):** fresh real-LLM evidence — model emits `level_up_now` WITHOUT `level_up_signal` (orphaned half-pair) → canonical session never forms. Prompt-first fix required pre-unfreeze; PR also CONFLICTING vs main (rebase needs force-push approval). Tempers rev-kf3q1: mixed-contract strips condemned (0/11) but partial-handoff handling has a live counterexample — deletion PR must carve it out.
- **#7452 cs-FAIL (6 items posted on PR):** sync unconditional (world_logic:8151) vs mode-gated guard (:7464) → strips legit fields on GOD/LEVEL_UP turns; audit-field rewrite destroys raw traces; unregistered surface; not in zfc-leveling API list; 3× duplication; Gate-6 link. /es + /er PASSED (its own real-LLM scenario passes at head). Level-6 mechanism PROVEN from production entries `FCRVHnE1`/`a29YQMFR` (campaign NFBaxQ3mIUe17UlAAGlE).
- **Tooling:** dark-factory `runner/handlers.py:1178` TimeoutExpired str/bytes crash patched (UNCOMMITTED in ~/projects/dark-factory); gate timeouts need ≥1500s for codex; evidence bundles under /tmp/worldarchitect.ai/factory-runs/ev3-*.

Related: [[levelup-cleanup-state-2026-06-10]], [[pr7447-dead-reducer-deletion-2026-06-10]].
