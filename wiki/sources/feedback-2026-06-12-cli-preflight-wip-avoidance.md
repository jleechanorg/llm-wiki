---
title: "CLI Preflight WIP-Avoidance — File-Disjoint Lane Pattern"
type: source
tags: [dark-factory, parallel-subagents, file-disjoint-lanes, preflight, claudeaf]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-dark-factory/memory/feedback_2026-06-12_cli_preflight_wip_avoidance.md
---

## Summary
When `runner/__main__.py` + `runner/handlers.py` are mid-edit by another workstream (e.g. `claudeaf` backend addition), scope a new workstream to NEW files only (`runner/preflight.py`) plus bash wrappers. The preflight returns structured JSON `{"status": "pass|warn|fail", "checks": [...], "fallback_recommendation": "codex"}` and bash wrappers gate entry BEFORE exec'ing Python.

## Key Claims
- `git diff --name-only HEAD` is the source of truth for "is this file in flight?" — not vibes, not memory.
- Lanes sharing ANY mutable file are NOT independent (compute via `git diff --name-only <base>...<branch>` or pairwise `git merge-tree --write-tree`).
- The fix: a NEW `runner/preflight.py` module with zero overlap with WIP'd files. The preflight is invoked from bash wrapper BEFORE runner Python runs.
- Exit code 2 on fail, exit 0 with stderr warning on warn.
- When the WIP'd file is the natural home for new behavior, route new behavior to a NEW file that the WIP'd file imports/uses, and modify the bash entrypoint instead.

## Key Quotes
> "The `claudeaf` WIP added `claudeaf` to backend choices in `__main__.py` and dispatch logic in `handlers.py`; stomping on those mid-edit creates a merge collision that takes hours to unwind. The fix: a NEW `runner/preflight.py` module that has zero overlap with the WIP'd files."

## Connections
- [[ParallelSubagents]] — independence check via file overlap
- [[BeadFollowupTemplates]] — workstream scoping
- [[StackedPRSingleWriter]] — file ownership rules
- [[ThermoSimplifyCrossValidation]] — 4-subagent fanout pattern
