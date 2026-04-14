# PR #2: Add benchmark run artifacts and orchestration helper scripts

**Repo:** jleechanorg/orchestrator_benchmark
**Merged:** 2026-03-12
**Author:** jleechan2015
**Stats:** +1057/-0 in 25 files

## Summary
- add local orchestration configs and helper scripts under `.claude/`, `agent-orchestrator.yaml`, and symphony overlay helpers
- add benchmark run artifacts for leetcode hard-5 benchmark runs
- add test fixtures and update local agent instructions/docs

## Raw Body
## Summary
- add local orchestration configs and helper scripts under `.claude/`, `agent-orchestrator.yaml`, and symphony overlay helpers
- add benchmark run artifacts for leetcode hard-5 benchmark runs
- add test fixtures and update local agent instructions/docs

## Notes
- excluded generated cache/history artifacts (`__pycache__`, `.beads/.br_history`) from this PR

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk: primarily adds benchmark artifacts, documentation, and local helper scripts/config without changing core runtime or production logic.
> 
> **Overview**
> Adds `.claude` PostToolUse hook tooling (`metadata-updater.sh` + settings) to auto-update agent-orchestrator session metadata when running common git/GitHub CLI commands, and introduces a local `agent-orchestrator.yaml` project config.
> 
> Checks in multiple benchmark run artifacts under `benchmarks/runs/` (specs, manifests, dispatch instructions, and `e2e10_results.tsv`) for LeetCode hard-5 and an alternate hard-5 set, and adds Symphony overlay helper workflows/scripts (`hello_world` smoke and `leetcode5` runner).
> 
> Updates benchmark agent/worker rules in `AGENTS.md`/`CLAUDE.md` to require a single terminal outcome per attempt, and adds JSON fixtures under `tests/fixtures/` for generic tasks and SWE-bench verified instances.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 4deb94c369bb042ca8f468b7da670aeab36500de. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

* **New Features**
  * Added four new benchmark tasks for orchestration testing
  * Introduced benchmark workflow specifications for LeetCode problem-solving scenarios
  * Added agent orchestrator configuration system with session metadata tracking
  * Added smoke test workflow for initial system 
