---
name: dark-factory-ao-spawn-lock-serializes
description: "dark-factory --backend ao serializes per AO project; 5 parallel pipelines targeting 'worldarchitect' all fail with 'Another ao spawn is in progress'. Use --backend claude for true parallel."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3c559681-688f-4e19-a369-9d9453805f13
---

When spawning multiple dark-factory pipelines in parallel targeting the SAME AO project, **only the first one succeeds** — every subsequent pipeline's `ao spawn` call returns `ao spawn failed (rc=1): ✗ Another ao spawn is in progress for project "worldarchitect" (PID N, started ...). Wait for it to finish.`

**Why**: AO CLI enforces a per-project spawn lock (single writer per project). When 5 parallel dark-factory pipelines all call `ao spawn -p worldarchitect`, AO serializes them. The lock is global to the AO daemon, not per-pipeline. So pipelines queue up and the first one in gets through; the rest fail at every codergen node (plan, implement, review, fix, gates).

**Symptoms**: 
- Only 1 of N parallel pipelines completes a full 36-step run.
- Others get stuck at `explore_in` / `plan` / `implement` with `ao spawn failed (rc=1)` after 1-2 successful nodes.
- `~/.dark-factory/merge_train/*.lock` files get orphaned for each lane.
- Evidence bundles exist but are tiny (21-48 events, not the full 154+ of a completed run).

**Fix** (use for parallel `/f` work):

1. **Switch to `--backend claude`** (or `agy` / `codex`). These backends shell out to `claude --print` / `agy --print` / `codex exec --yolo` directly per node — no AO spawn, no per-project lock. The pipelines run truly in parallel.

2. Drop `--ao-project` and `--ao-agent` flags (AO-specific, not needed for `claude` backend).

3. The dark-factory pipeline still progresses through nodes (start → explore → plan → implement → test → review → holdout → gates → exit) sequentially within each pipeline. "Parallel" is at the teammate level (N Claude teammates each running dark-factory), not at the codergen node level.

4. If you must use `ao` backend, run pipelines **sequentially** (one at a time). The AO lock will serialize them anyway, so you save the per-spawn overhead by accepting the serial cost.

**Why we tried 5 parallel and it didn't work (2026-06-13)**: Spawned 5 `/f` pipelines targeting `worldarchitect` simultaneously. Only PR-5 won the lock and ran a full 36-step pipeline. The other 4 (pr2, pr3, pr4, pra) each grabbed the lock for one node, then blocked on subsequent nodes. After clearing the orphaned `~/.dark-factory/merge_train/*.lock` files and switching all 4 to `--backend claude`, they should run in parallel.

**How to apply**: When dispatching multiple `/f` pipelines in parallel for the same AO project, use `--backend claude` (NOT `ao`) to avoid the spawn lock. The `claude` / `agy` / `codex` backends are direct shell-outs and have no global lock. This is the only way to get true parallelism in dark-factory today.

**Diagnostic command**:
```bash
grep -E "Another ao spawn" /tmp/dark-factory/<lane>-run.log
# or
tail /tmp/dark-factory/evidence-<lane>/events.jsonl | grep -E "Another ao spawn"
```
