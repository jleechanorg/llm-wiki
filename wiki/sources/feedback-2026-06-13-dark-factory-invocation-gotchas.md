---
title: "2026-06-13 Dark Factory Invocation Gotchas"
type: source
tags: ["feedback", "worldarchitect", "dark-factory", "agent-orchestrator"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_dark_factory_invocation_gotchas.md
---

## Summary
Three persistent dark-factory /f invocation gotchas — cwd must be df root (not worktree), --ao-project worldarchitect (no .ai), sealed holdout fail-closed is correct

## Key Claims
- `dark-factory --pipeline <.dot> ...` has three persistent invocation gotchas that surface on first /f run per session:
- 1. **`cwd` must be the dark-factory project root** (`/Users/jleechan/projects/dark-factory`), NOT the lane's `--workdir`. The include parser (`runner/parser.py:407`) tries `parent_dir / ref` then `cwd / ref` to resolve `@pipelines/_base.dot`; it does NOT try the df project root. When invoked from a worktree cwd, the include fails with `ValueError: ... include not found: 'pipelines/_base.dot'`. `--workdir` is unchanged (the actual feature work still happens in the lane worktree). The cwd change only affects include resolution.
- 2. **`--ao-project` is `worldarchitect` (no `.ai`)** for the worldarchitect.ai repo. The available AO project list: `agent-orchestrator, agf-api, agf-lambda, claude-commands, cmux, dark-factory, heretic-lab, jleechanclaw, mcp-mail, mctrl-test, merge_train, openclaw-sso, ralph, smartclaw, worldai-claw, worldarchitect`. Parameter-fidelity rule: do NOT silently substitute — if a brief says `worldarchitect.ai`, stop and report the actual list.
- 3. **Sealed holdout fail-closed is correct behavior.** The `holdout` phase in `minimal_feature_cs.dot` and similar pipelines points at `~/projects/dark-factory-holdouts/` which is operator-run only. When the implementing agent hits it, the pipeline fails closed (does NOT bypass) and routes to `fix`. The fix loop will continue until `max_retries` or `max_visits` is exhausted, OR an operator unblocks the holdout. Do not try to bypass.

## Connections
- [[WorldarchitectAI]] — worldarchitect.ai project memory
- [[DarkFactory]] — dark-factory pipeline memory
- [[AgentOrchestrator]] — AO worker dispatch memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_dark_factory_invocation_gotchas.md`
