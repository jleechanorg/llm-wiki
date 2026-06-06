# Evidence review — exclude structurally-unmeasurable axes from "no separation on any axis" (2026-06-05)

**Type:** feedback / evidence-review discipline
**Origin:** `/er` (evidence_review) on [PR #16](https://github.com/jleechanorg/dark-factory/pull/16) — dark-factory, head `b2bd7a3`
**Bead:** `jleechan-g8m` (closed) · **Memory:** `feedback_2026-06-05_evidence_review_unscorable_axes.md`
**Verdict:** PASS (first-party re-verify + independent `evidence-reviewer` subagent agreed; suite 226 green)

## The lesson

A benchmark reported "no separation on **any** axis" for an A-vs-A+B null, but the
committed aggregate (`benchmarks/workflow_graphgen/results/n10_aggregate.json`)
marked one of the five axes — `graph_quality` — as `n=0 / insufficient data`
(`score=None, unscored=True`). That axis is **structurally mode-invariant**: both
modes consume the *same* graph-IR, so the fit score (computed once per goal, reused)
**cannot** separate by construction.

The team already knew this (the spec memory wrote "graph_quality mode-invariant by
construction (shared IR)"), yet the cross-bench synthesis prose folded it into a
blanket "any axis" null. **The aggregate JSON was honest; the one-line summary
outran it.**

## Rule

When reporting a "no separation on any axis" null, **partition axes into
{measured-and-tied} vs {unscorable / structurally invariant}** and exclude the
latter from "any." A null on an axis that *cannot* separate is zero evidence of
equivalence — it is a non-measurement. Trust the aggregator's `insufficient data` /
`winner=null` distinction; never let a prose roll-up erase it.

## Generalizable evidence-review heuristics (confirmed)

1. **True-negative requires a sighted ruler.** Prove the instrument can detect an
   effect by reusing the *same* aggregator (`benchmarks.workflow_graphgen.scoring.aggregate`)
   on engineered scenarios where it credits winners (dynamic_fanout credited 4).
   Grep the import to confirm it's literally the same function.
2. **Weakest-link-first.** Does the null have a *committed records artifact* or only
   prose? Here: 40 records, 20/mode, `model_name=claude-sonnet-4-6`, per-trial git refs.
3. **Real-vs-model disclosure audit.** dynamic_fanout tokens are a deterministic
   call-count model (disclosed), not billing — disclosure keeps it honest.
4. **Name the negative space.** wall_ms A+B ~5–9% slower was correctly *not credited*
   (ranges overlap at n=10); non-adjacent state threading still needs a 1-line engine change.

## Relevance

Refines [[EvidenceBasedVerification]] and [[CalibrationBiasVerification]]. Does **not**
affect [[jeffrey-oracle]] (technical workflow learning). Related:
[[feedback_2026-05-29_evidence_sha_staleness]].

## References

- PR: https://github.com/jleechanorg/dark-factory/pull/16 (head `b2bd7a3`)
- `benchmarks/FINDINGS.md` Finding 1; `benchmarks/workflow_graphgen/results/n10_aggregate.json`
- `benchmarks/dynamic_fanout/` (same-aggregator calibration, 4 winners)
- Verify: `.venv/bin/python -m pytest tests/` → 226 passed; subset 32 passed
