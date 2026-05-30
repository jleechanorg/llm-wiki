---
name: Dark Factory brownfield-vs-greenfield pipeline flaws (+ timeout false-success, shared-cxdb, collision OPTION-2)
description: Four durable learnings from the WorldArchitect.AI conclude-finalize Dark Factory session — timeout false-success, shared CXDB cross-contamination, collision OPTION-2 preference, and the headline brownfield-run-as-greenfield root cause.
type: feedback
bead: rev-kq9cf
---

# Dark Factory brownfield-vs-greenfield pipeline flaws

Session: WorldArchitect.AI Dark Factory "conclude-finalize prompt" run, 2026-05-30.
Governing PR: [#7178](https://github.com/jleechanorg/worldarchitect.ai/pull/7178) (Path B, replaces [#7175](https://github.com/jleechanorg/worldarchitect.ai/pull/7175)).
Canonical Dark Factory runner: `/Users/jleechan/projects/dark-factory/runner/handlers.py`.
Brownfield pipeline DOT: `/tmp/conclude_brownfield.dot`. CXDB run id: `a147c7bdeaf9`.

Four sub-lessons captured together because they all surfaced in one run and reinforce each other.

---

## 1. TIMEOUT-CRASH FALSE-SUCCESS  (Anti-Pattern)

**Context.** The Dark Factory `_tool` handler shells out to a deterministic command
and bounds it with a subprocess timeout:

```python
# runner/handlers.py (~line 577, the _tool handler; subprocess.run at ~line 597)
timeout = int(node.attrs.get("timeout", "300"))
...
proc = subprocess.run(..., timeout=timeout)
```

**Failure.** A real-LLM test node legitimately runs longer than the default 300s.
When it does, `subprocess.run` raises `subprocess.TimeoutExpired` and **crashes the
run**. Worse, `runs.final` was left at `'success'` at crash time, so a naive monitor
that read `runs.final` mis-reported the run as successful.

**Rule / fix.**
- Set `timeout="2400"` (or higher) on any long real-LLM node attrs. The 300s default
  is unsafe for real model calls.
- A monitor must declare **DONE only when the `exit` node is recorded in the `steps`
  table** for that run. NEVER infer DONE from `runs.final` — `runs.final` can hold a
  stale `'success'` from before a crash.

## 2. SHARED-CXDB CROSS-CONTAMINATION  (Anti-Pattern)

**Context.** Dark Factory's CXDB lives at `~/.dark-factory/cxdb.sqlite` and is
**shared across all concurrent runs** (any agent, any pipeline).

**Failure.** A monitor that queried "the latest run" latched onto a **different
agent's unrelated run** — an `agf-api` run `24e130dcdc14` — and reported on the wrong
work entirely.

**Rule / fix.** Always pin monitoring and CXDB queries by **exact `run_id`**:

```sql
SELECT ... FROM steps WHERE run_id = 'a147c7bdeaf9';
```

Never use "latest run", `ORDER BY ts DESC LIMIT 1`, or any implicit-recency selector
against the shared CXDB.

## 3. COLLISION-POLICY OPTION-2  (Best Practice — standing user preference)

When two of the user's own agents collide on the same branch, the default resolution
is **OPTION 2**:

1. Let the running work finish (do not kill it mid-flight).
2. Rebase onto the other agent's commit.
3. Keep **BOTH** fixes.
4. **ALWAYS review both fixes for correctness** before accepting.

Never blindly discard either side. This is a durable preference, not a one-off call.

## 4. BROWNFIELD-VS-GREENFIELD FACTORY FLAW  (Critical / Anti-Pattern — the headline)

**Root cause.** A **brownfield** refactor/replace/DELETE task — replace the backend
force-override with a model-owned `conclude` prompt — was run through a **greenfield,
additive** Dark Factory pipeline. The pipeline shape can only add; it has no machinery
to remove a running code path.

**Three concrete failures it produced:**

- **(a) Orphaned deletion.** The override removal was staged as a *conditional*
  "after proof, delete X" inside the `implement` goal — but **no DAG node executes a
  post-proof deletion**, and the resume pipeline had **no `implement` node at all**.
  The deletion simply never ran.
- **(b) Backwards proof staging.** The old override was **still present during the
  real-LLM proof**, so a green verdict proved nothing — the old fallback could mask a
  weak new path. You must prove against the **post-deletion** tree.
- **(c) Dead code passed `test_e2e`.** A Pydantic `ConcludeSnapshot` model was
  unit-tested but **never wired to a runtime call site**, yet `test_e2e` went green.
- **Net result:** diff was **+2507 / −54 with ZERO override deletion** for a task whose
  entire point was deletion.

**Fix (durable, already applied this session).** Added a mandatory **"Step 0: classify
Brownfield vs Greenfield"** section to `~/.claude/skills/factory-spec/SKILL.md` with
6 brownfield rules:

1. **DELETE-FIRST ordering** (not delete-last): the `implement` node must remove/replace
   the old path, not defer it.
2. **Deletion needs an executor node** — never a conditional/comment. A node must
   actually perform the removal.
3. **Net-LOC ≤ 0 guard** for replace/delete milestones (gate/acceptance check).
4. **Dead-code gate** — FAIL if a newly-added symbol is defined-but-unreferenced at
   runtime.
5. **Replace at the same call site** — the new path must be wired where the old one was.
6. **Prove against the post-deletion tree** — run the real-LLM proof after the old path
   is gone.

**Quick test to classify any milestone:** *"If this milestone succeeds, should
`git diff` show deletions?"* → **yes → brownfield** → apply rules 1–6. If the planned
diff is all additions for a replace/delete goal, the pipeline is mis-shaped — STOP and
re-architect delete-first.

---

## Reusable pattern

- **For any factory/automation pipeline run:** classify brownfield vs greenfield at
  Step 0. Brownfield deletes must be ordered first, executed by a real node, guarded by
  net-LOC ≤ 0 and a dead-code gate, wired at the same call site, and proven against the
  post-deletion tree.
- **For any monitor over a shared store:** pin by exact run id; declare DONE only from a
  terminal record (the `exit` step), never from a mutable summary field like
  `runs.final`.
- **For real-LLM nodes:** raise subprocess timeouts well above the 300s default
  (≥2400s).
- **For agent-vs-agent branch collisions:** OPTION-2 — finish, rebase, keep both, review
  both.

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7178 (Path B, replaces #7175)
- `/Users/jleechan/projects/dark-factory/runner/handlers.py` — `_tool` handler timeout
  default at ~line 577; `subprocess.run` at ~line 597; lines 550-560 region for `_tool`
  docstring/setup.
- `~/.claude/skills/factory-spec/SKILL.md` — Step 0 brownfield-vs-greenfield section
  (rules 1-6).
- `/tmp/conclude_brownfield.dot` — the brownfield pipeline graph.
- CXDB: `~/.dark-factory/cxdb.sqlite` (shared); run `a147c7bdeaf9`; contaminating run
  `24e130dcdc14` (agf-api).
- Bead: `rev-kq9cf` (closed, labels: learning, documentation).
