# Source: Dark Factory brownfield-vs-greenfield pipeline flaws (2026-05-30)

- **Type**: feedback / learning
- **Date**: 2026-05-30
- **Origin**: WorldArchitect.AI Dark Factory "conclude-finalize prompt" session
- **Raw**: `~/llm_wiki/raw/feedback_2026-05-30_dark_factory_brownfield_flaws.md`
- **Claude memory**: `/Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree-level-not-registered/memory/feedback_2026-05-30_dark_factory_brownfield_flaws.md`
- **Bead**: rev-kq9cf (closed; learning, documentation)
- **PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/7178 (Path B, replaces #7175)

## Summary

Four durable learnings surfaced in one [[DarkFactory]] run.

### 1. Timeout false-success (Anti-Pattern)
The `_tool` handler bounds shell-outs with `timeout = int(node.attrs.get("timeout","300"))`
(`runner/handlers.py` ~line 577; `subprocess.run` at ~597). A real-LLM node exceeding 300s
raises `subprocess.TimeoutExpired` and crashes the run; `runs.final` stayed `'success'`, so a
naive monitor mis-reported success. **Fix:** set `timeout="2400"`+ on long real-LLM nodes;
declare DONE only when the `exit` node is in the `steps` table, never from `runs.final`.

### 2. Shared-CXDB cross-contamination (Anti-Pattern)
[[CXDB]] at `~/.dark-factory/cxdb.sqlite` is shared across all concurrent runs. A "latest run"
query latched onto an unrelated `agf-api` run `24e130dcdc14`. **Fix:** always pin by exact
`run_id` (`where run_id='a147c7bdeaf9'`), never "latest run".

### 3. Collision OPTION-2 (Best Practice — standing user preference)
When two of the user's agents collide on a branch: let running work finish, rebase onto the
other agent's commit, keep BOTH fixes, ALWAYS review both for correctness. Never blindly discard.

### 4. Brownfield-run-as-greenfield (Critical / Anti-Pattern — headline)
A brownfield DELETE task (replace backend force-override with a model-owned conclude prompt) ran
through a greenfield additive pipeline. Results: (a) orphaned deletion — conditional delete-last,
no executor node, resume pipeline had no implement node; (b) backwards proof staging — old override
present during real-LLM proof so green proved nothing; (c) dead code passed test_e2e — a Pydantic
`ConcludeSnapshot` model unit-tested but never wired to a runtime call site. Net +2507/−54 with
ZERO deletion. **Fix (applied):** Step 0 brownfield-vs-greenfield classification added to
`~/.claude/skills/factory-spec/SKILL.md` with 6 rules — DELETE-FIRST ordering, deletion needs an
executor node (not a conditional), net-LOC ≤ 0 guard, dead-code gate, replace at same call site,
prove against the post-deletion tree. Quick test: "if this milestone succeeds, should git diff
show deletions?" → yes → brownfield.

## Related concepts
- [[DarkFactory]]
- [[CXDB]]

## jeffrey-oracle
Does not affect `[[jeffrey-oracle]]` — this is a technical workflow/harness learning.
