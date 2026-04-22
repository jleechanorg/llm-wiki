# Nextsteps — Project Chimera — 2026-04-21

## Table of contents

- [Executive summary](#executive-summary)
- [Context](#context)
- [Bead index](#bead-index)
- [Work queue](#work-queue)
- [Evidence review findings](#evidence-review-findings)
- [Rubric redesign](#rubric-redesign)
- [Learnings pointer](#learnings-pointer)
- [Roadmap pointer](#roadmap-pointer)

## Executive summary

- **Outcomes**: P4 Run 3 complete (292.6 min, 15/15 queries). All infrastructure fixes committed (`84a973c`). Evidence bundle now clean — SHA checksums verified, pairwise data re-parsed, metadata with provenance.
- **Key findings**:
  1. Original 4.1/3.8/1.5 stats FABRICATED — actual (excluding errors): single=4.73, fixed=5.00, gnn=5.03
  2. Multi-agent 100% reliable (fixed/gnn 0% errors) vs single 86.7% (2/15 timeouts)
  3. **Rubric ceiling at 5.0** — 14/15 queries score 5.0 regardless of content. Quality comparison INCONCLUSIVE.
- **Blocker**: Rubric saturates at 5.0 — cannot discriminate quality above "adequate." Need redesign with behavioral anchors, asymmetric descriptors (5=floor not ceiling), pairwise tiebreaking.
- **Next**: Design and implement new rubric, then re-run benchmark.
- **Repo**: `~/autowiki/` | `https://github.com/jleechanorg/autowiki`

## Context

Project Chimera is a 22-agent GNN-driven LLM swarm. This session:
1. Fixed pairwise JSON corruption (`0c41e23`, `5ce5e06`) — re-parsed 45 pairwise entries
2. Fixed aggregate script to use checkpoint error_flag (`6e1d10d`)
3. Updated evidence bundle: SHA checksums, metadata provenance, evidence.md (`84a973c`)
4. Ran /research and /secondo on rubric design — found root cause: rubric treats 5 as ceiling not floor

**Evidence verdict**: Error rates DEFENSIBLE. Quality comparison INCONCLUSIVE (rubric ceiling).

## Bead index

No Chimera-specific beads. Issues tracked in repo at `https://github.com/jleechanorg/autowiki`.

## Work queue

### P1 — Revoke exposed API key ⚠️ USER ACTION STILL REQUIRED
- **Status**: Key removed from code, still active at MiniMax dashboard
- **Key**: `sk-cp-Rg64...` (see prior nextsteps for full value)
- **Action**: MiniMax dashboard → API keys → revoke

### P2 — ✅ DONE — Retry logic
- **Files**: `chimera/utils.py`, `run_hard_benchmark.py` (commits `fb78717`, `6e1d10d`)
- **Changes**: 3-attempt exp backoff (1s→2s→4s), 180s timeout, circuit breaker after >3 consecutive failures

### P3 — ✅ DONE — Rubric error calibration
- **Files**: `chimera/judge.py`, `run_hard_benchmark.py` (commit `fb78717`)
- **Changes**: `_is_error_output()` detects API errors (first 500 chars only), returns `{"is_error": true, "overall": 0.0}`, errors excluded from averages

### P4 — ✅ DONE (Run 3) — Benchmark complete but rubric ceiling blocks conclusions
- **Files**: `run_hard_benchmark.py`, `benchmark_logs/`
- **Results**: single=4.73 (2 errors), fixed=5.00 (0 errors), gnn=5.03 (0 errors)
- **Problem**: 14/15 queries score 5.0 — rubric cannot discriminate quality
- **Next**: Re-run with redesigned rubric

### P5 — ✅ DONE — Aggregation script fixed
- **Files**: `aggregate_benchmark.py` (commits `6e1d10d`, `84a973c`)
- **Fix**: Uses checkpoint error_flag (500-char-limited patterns), reads from checkpoint.json

### P6 — ✅ DONE — Evidence bundle cleaned
- **Files**: `benchmark_logs/` (commit `84a973c`)
- **Files**: `evidence.md`, `checksums_final.sha256`, `metadata.json` (with provenance fields)

### P7 — ✅ DONE — Redesign rubric to break 5.0 ceiling
- **Files**: `chimera/judge.py`, `run_hard_benchmark.py` (commit `7b59ce9`)
- **Changes**: 6-dimension rubric (100pts), Insight heaviest (25pts), 5=floor not ceiling, behavioral anchors for 8+, accuracy gate caps at 3/10, 500-char error detection, pairwise tiebreaking
- **Acceptance criteria**: Score distribution spans at least 3 points across 15 queries — pending P8 re-run

### P8 — ⬜ NEW — Re-run benchmark with new rubric
- **Goal**: Get valid quality comparison between GNN, Fixed, Single modes
- **Files**: `run_hard_benchmark.py`, `benchmark_logs/`
- **Acceptance criteria**: Error rate <5% per mode, score distribution spans 3+ points, pairwise comparisons show discriminable winners

## Evidence review findings

**Defensible conclusions** (error rates, reliability):
- Multi-agent is more reliable: fixed/gnn 0% errors vs single 13.3% (2 timeouts)
- Original 4.1/3.8/1.5 were FABRICATED — actual 4.73/5.00/5.03
- 8 retries with exponential backoff confirmed in log

**Inconclusive conclusions** (quality comparison):
- GNN vs Fixed vs Single quality: cannot determine due to rubric ceiling
- The 0.03pt GNN advantage (5.03 vs 5.00) is one query's rounding, not architecture
- Pairwise comparisons partially recovered but still noisy

**Rubric ceiling mechanics**:
- 14/15 queries produce overall=5.0 regardless of content
- Score range for Fixed is literally 5.0-5.0 (zero variance)
- The rubric criteria are too easy to satisfy — "has citations" earns partial credit, "covers topic" earns partial credit
- An LLM judge satisfies all criteria at minimum viable level

## Rubric redesign

**Core principle**: Every score level needs specific, observable behaviors. If you can't write "what the report actually says or does" that earns 8 vs what earns 5, the rubric is not calibrated.

### Proposed 6-dimension rubric (100 pts)

| Dimension | Pts | 5=baseline | 8+=exceptional |
|-----------|-----|------------|----------------|
| Factual Accuracy + Uncertainty Honesty | 15 | All accurate, no fabricated citations | Accurate + explicitly flags uncertainty, distinguishes speculation from evidence |
| Coverage Breadth + Depth | 20 | Covers all major subtopics, surface level | All + edge cases, counterarguments, open questions within each |
| **Insight and Analytical Originality** | **25** | Logical connections, appropriate conclusions | **Non-obvious relationships, synthesizes across sources in ways they don't do themselves** |
| Evidence Chain Quality | 15 | Cites sources, supports claims | Primary sourcing, explicit evidence→inference→conclusion chain |
| Actionability | 15 | Vague recommendations | Specific action + owner + conditions + verification |
| Structure + Readability | 10 | Clear baseline, section headers | Executive summary, value-add tables, excellent hierarchy |

### Key design choices to prevent saturation

1. **5 is a FLOOR not ceiling**: 5="meets baseline." 8="does something non-obvious." Gap between 5→8 is behavioral, not just "better."
2. **Explicit 8+ anchors**: Report must exhibit at least one specific behavior (e.g., "identified a contradiction between sources") to score 8+
3. **Accuracy gate**: If accuracy=0 (dangerous inaccuracies), max composite score capped at 3/10
4. **Pairwise tiebreaking**: When absolute scores within 0.5pt, fall back to head-to-head comparison
5. **Bonus for exceptional**: +2pts for reports that do something genuinely non-obvious (found contradiction, provided working code example, identified query framing limitation)

### Absolute vs pairwise

Use **absolute scoring primary** (interpretable, self-contained) with **pairwise tiebreaking** when scores cluster within 0.5pt. Bradley-Terry scaling produces total ordering even when absolute scores saturate.

## Learnings pointer

- `~/roadmap/learnings-2026-04.md` — section `2026-04-21 — Chimera P4: rubric ceiling prevents quality comparison`

## Roadmap pointer

- `llm_wiki/roadmap/README.md` — Recent activity (rolling) section updated
- Repo: `https://github.com/jleechanorg/autowiki`
