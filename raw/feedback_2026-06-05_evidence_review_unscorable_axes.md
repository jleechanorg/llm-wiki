---
name: Evidence review — exclude structurally-unmeasurable axes from "no separation on any axis"
description: A null on an axis that cannot separate by construction is not evidence of equivalence; synthesis prose must preserve the aggregate's "insufficient data" distinction.
type: feedback
bead: jleechan-g8m
metadata:
  node_type: memory
  type: feedback
  originSessionId: 96237b72-565c-4c2d-b265-b151de9c2353
---

**Context:** `/er` (evidence_review) on [PR #16](https://github.com/jleechanorg/dark-factory/pull/16) (dark-factory, head `b2bd7a3`) — the workflow_graphgen n=10 null + dynamic_fanout calibration ([[project_2026-06-05_dynamic_fanout_calibration]], [[project_2026-06-04_workflow_graphgen_spec]]). Verdict: **PASS** (first-party re-verify + independent `evidence-reviewer` subagent agreed; 226 suite green; n=10 backed by a *committed* records artifact `benchmarks/workflow_graphgen/results/n10_records.jsonl` + `n10_aggregate.json`, real `model_name=claude-sonnet-4-6`, per-trial git refs — not prose).

**The lesson (Best Practice / mild Anti-Pattern):** `benchmarks/FINDINGS.md` Finding 1 says "no separation on **any** axis," but `n10_aggregate.json` marks `graph_quality` as `n=0 / insufficient data` for both features — every record has `graph_quality.score=None, unscored=True`. That axis is **structurally mode-invariant**: both Mode A and Mode A+B consume the *same* graph-IR, so the fit score (computed once per goal, reused) **cannot** separate by construction. The team already knew this — the spec memory literally wrote "graph_quality mode-invariant by construction (shared IR)" — yet the cross-bench synthesis prose folded it into a blanket "any axis" null. **The aggregate JSON was honest; the one-line summary outran it.**

**Rule:** When reporting a "no separation on any axis" null, **partition axes into {measured-and-tied} vs {unscorable / structurally invariant}** and exclude the latter from "any." Precise claim here = "no separation on every *measured* axis (4/5); the 5th is unscorable by construction." A null on an axis that *cannot* separate is zero evidence of equivalence — it's a non-measurement. Trust the aggregator's `insufficient data` / `winner=null` distinction; never let a prose roll-up erase it.

**Generalizable evidence-review heuristics confirmed this session:**
- A "true negative" claim requires the *same* instrument crediting a winner elsewhere. dynamic_fanout proved the ruler isn't blind by importing the literal same `benchmarks.workflow_graphgen.scoring.aggregate` (grep the import to confirm — `driver.py` + `test_dynamic_fanout.py`) and crediting 4 winners.
- Verify the *weakest* link first: does the null have a committed records file, or only prose? Here it did (40 records, 20/mode, real metering shape).
- Distinguish real metering from a model: dynamic_fanout tokens are a deterministic **call-count model** (disclosed in RESULTS.md), NOT billing — that disclosure is what keeps it honest, not a defect.
- State the negative space: wall_ms A+B ~5–9% slower was correctly **not credited** (ranges overlap at n=10); non-adjacent state threading (node N←N−5) still needs a 1-line engine change.

**Verification:** `.venv/bin/python -m pytest tests/test_dynamic_fanout.py tests/test_dynamic_fanout_sweep.py tests/test_state_threading.py -q` → 32 passed; full `tests/` → 226 passed. `python3 -c` over `n10_aggregate.json` → 0 non-null winners across 2 features × 5 axes; `graph_quality` n=0 both.

**Reusable pattern:** evidence review of any A/B mechanism benchmark = (1) weakest-link-first artifact check, (2) same-instrument calibration for true-negative claims, (3) real-vs-model disclosure audit, (4) **axis partition: measured-tied vs structurally-unscorable**, (5) name what is NOT proven.
