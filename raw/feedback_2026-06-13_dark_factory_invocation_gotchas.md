---
name: dark-factory-invocation-gotchas
description: "Three persistent dark-factory /f invocation gotchas — cwd must be df root (not worktree), --ao-project worldarchitect (no .ai), sealed holdout fail-closed is correct"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3c559681-688f-4e19-a369-9d9453805f13
---

`dark-factory --pipeline <.dot> ...` has three persistent invocation gotchas that surface on first /f run per session:

1. **`cwd` must be the dark-factory project root** (`/Users/jleechan/projects/dark-factory`), NOT the lane's `--workdir`. The include parser (`runner/parser.py:407`) tries `parent_dir / ref` then `cwd / ref` to resolve `@pipelines/_base.dot`; it does NOT try the df project root. When invoked from a worktree cwd, the include fails with `ValueError: ... include not found: 'pipelines/_base.dot'`. `--workdir` is unchanged (the actual feature work still happens in the lane worktree). The cwd change only affects include resolution.

2. **`--ao-project` is `worldarchitect` (no `.ai`)** for the worldarchitect.ai repo. The available AO project list: `agent-orchestrator, agf-api, agf-lambda, claude-commands, cmux, dark-factory, heretic-lab, jleechanclaw, mcp-mail, mctrl-test, merge_train, openclaw-sso, ralph, smartclaw, worldai-claw, worldarchitect`. Parameter-fidelity rule: do NOT silently substitute — if a brief says `worldarchitect.ai`, stop and report the actual list.

3. **Sealed holdout fail-closed is correct behavior.** The `holdout` phase in `minimal_feature_cs.dot` and similar pipelines points at `~/projects/dark-factory-holdouts/` which is operator-run only. When the implementing agent hits it, the pipeline fails closed (does NOT bypass) and routes to `fix`. The fix loop will continue until `max_retries` or `max_visits` is exhausted, OR an operator unblocks the holdout. Do not try to bypass.

**Why**: 2026-06-13 first-round /f iteration on level-up v2 train — all 5 lanes (`pra`, `pr2`, `pr3`, `pr4`, `pr5`) panicked on first try at the same `include not found` error. Re-spawned with `cd /Users/jleechan/projects/dark-factory` and the second batch passed preflight. Then the implement/fix nodes hit `Unknown project: worldarchitect.ai` because the brief I was working from used the `.ai` suffix; the f-pipeline-pr4 teammate held parameter-fidelity (per `ao-operator-discipline` skill) and stopped. Third batch with `--ao-project worldarchitect` reached the holdout phase, which fail-closed correctly. The `merge_train` lock files in `~/.dark-factory/merge_train/*.lock` get orphaned on panic; clear them with `rm -f ~/.dark-factory/merge_train/*.lock` if preflight errors with `is held by run_id=...`.

**How to apply**: When spawning a /f pipeline teammate, the dark-factory invocation MUST start with `cd /Users/jleechan/projects/dark-factory && ...` (NOT `cd <workdir> && ...`). Pass `--ao-project worldarchitect` for the worldarchitect.ai repo. Set `--max-steps 60` or higher to give the explore fanout + fix loop room. Expect sealed-holdout fail-closed; do not interpret it as a bug. Run `rm -f ~/.dark-factory/merge_train/*.lock` if preflight errors with "is held by".
