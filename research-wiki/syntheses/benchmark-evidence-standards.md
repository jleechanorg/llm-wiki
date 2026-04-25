# Benchmark Evidence Standards

**Purpose**: Evidence standards for autor benchmark runs (P-series: P11, P12, P13, P14, P15).
This is a **subset** of the full `evidence-standards.md` — benchmark results do NOT require video/gif evidence.

## When This Applies

- P-series benchmark runs (mode routing, technique comparison, aggregate scoring)
- Research cycle experiments (ET, SR, PRM, SWE-bench comparison)
- Any run whose purpose is **score aggregation** rather than behavioral demonstration

## When NOT This Applies

- Integration/functional tests with behavioral claims → use full `evidence-standards.md`
- E2E claims requiring terminal video → use full `evidence-standards.md`
- PR lifecycle evidence → use full `evidence-standards.md`

---

## Required Files

Every benchmark run MUST produce:

| File | Purpose | Required Fields |
|------|---------|-----------------|
| `metadata.json` | Run provenance | `run_id`, `timestamp_utc`, `technique`, `mode`, `git_sha`, `git_branch`, `query_count`, `error_rate` |
| `scores/<mode>_<query>_<ts>.json` | Per-query scores | `score`, `latency`, `error`, `mode`, `query` |
| `aggregate.json` | Summary stats | `mean`, `stdev`, `n`, `win_counts`, `mode_summary` |
| `checksums.sha256` | Integrity verification | SHA256 of all score JSONs |

### metadata.json Schema

```json
{
  "run_id": "P14-20260423T030521Z",
  "timestamp_utc": "2026-04-23T03:05:21Z",
  "technique": "mode-router",
  "mode": "fixed|gnn|router|single",
  "git_sha": "86cc8070",
  "git_branch": "llm_chimera",
  "query_count": 15,
  "error_rate": 0.0,
  "checksum_mode": "aggregate_sha256",
  "benchmark": "chimera-mode-router-v1"
}
```

### Per-Query Score Schema (e.g., `scores/P14_Q1_fixed_20260424T024534Z.json`)

```json
{
  "query": "Q1",
  "mode": "fixed",
  "score": 50.0,
  "latency": 18.2,
  "error": null,
  "timestamp": "2026-04-24T02:45:34Z",
  "run_id": "P14-20260423T030521Z",
  "rubric_version": "6-dim-v3",
  "max_score": 121.75
}
```

### aggregate.json Schema

```json
{
  "run_id": "P14-20260423T030521Z",
  "mode_summary": {
    "fixed": { "n": 21, "mean": 62.98, "stdev": 24.3, "min": 0, "max": 121.75, "latency_mean": 18.2 },
    "gnn": { "n": 21, "mean": 58.55, "stdev": 20.94, "min": 0.0, "max": 80.75, "latency_mean": 23.47 },
    "router": { "n": 21, "mean": 43.21, "stdev": 30.93, "min": 0.0, "max": 82.25, "latency_mean": 26.89 },
    "single": { "n": 21, "mean": 15.67, "stdev": 22.78, "min": 0.0, "max": 59, "latency_mean": 19.18 }
  },
  "win_counts": { "fixed": 5, "gnn": 7, "router": 3, "single": 0 },
  "error_rate_per_mode": { "fixed": 0.0, "gnn": 0.0, "router": 0.0, "single": 0.0 },
  "query_count": 15,
  "timestamp": "2026-04-23T12:00:00Z"
}
```

---

## Checksum Requirements

**Aggregate checksum only** (not per-file checksums for benchmark scores):

```bash
# Generate aggregate checksum AFTER all score JSONs are written
sha256sum scores/*.json aggregate.json metadata.json > checksums.sha256

# Verify
sha256sum -c checksums.sha256
```

**Per-file checksums are NOT required** for individual score files — use aggregate mode to reduce file churn. The `.sha256` file itself is the evidence; individual score integrity is validated by the aggregate.

---

## No Video/GIF Required

Benchmark results do NOT require:
- Terminal video captures
- GIF evidence
- asciinema recordings
- Session replays

**Rationale**: Benchmark runs are scored numerically against a rubric. The score JSONs ARE the evidence. Video adds no information to a score comparison.

Exception: If a benchmark run makes a **behavioral claim** (e.g., "the router correctly identified X"), a single 10-second GIF showing the router's output is sufficient — but it is not mandatory.

---

## Error Rate Reporting (MANDATORY)

Per the Benchmark Reliability Gate:

1. **Error rate per mode MUST be reported** alongside quality scores
2. **Error-state outputs must be distinguished** from valid outputs in the rubric (API errors score 0 or 1, not the same as mediocre valid output)
3. **Summary statistics must be computed by script**, not typed from memory

**Error rate threshold**: If any mode has >5% error rate, the aggregate.json MUST include:
```json
{
  "error_rate_per_mode": { "fixed": 0.0, "gnn": 0.067, "router": 0.0 },
  "caveat": "results dominated by API errors — quality superiority claims excluded"
}
```

---

## Logging Requirements

Benchmark runs do NOT require individual et_logs per query. Only:
- One aggregate log file per technique run
- Error traces for failed queries

```
research-wiki/
  scores/
    P14_Q1_fixed_20260424T024534Z.json
    P14_Q1_gnn_20260424T024642Z.json
    ...
  logs/
    P14_aggregate_20260424T040000Z.log
```

---

## Commit-before-Run Protocol (from P15)

1. Commit all code changes BEFORE running benchmark
2. Create `metadata.json` with git SHA
3. Run benchmark
4. Write aggregate.json and checksums.sha256
5. Push results

**Anti-pattern**: Creating provenance artifacts after the run completes (post-hoc metadata).

---

## P14: Verified Run

**Run ID**: P14-20260424T030521Z
**Status**: ✅ Complete — all standards met

| Check | Status |
|-------|--------|
| `metadata.json` | ✅ `run_id`, `timestamp_utc`, `git_sha`, `error_rate=0.0` |
| All 84 score JSONs in `scores/` | ✅ 15 queries × 4 modes + 9 hybrid = 84 files |
| `aggregate.json` with mode_summary, win_counts | ✅ |
| `error_rate_per_mode` reported | ✅ All modes 0.0% |
| `checksums.sha256` generated after all files | ✅ 86 entries verified |
| No video/gif required | ✅ Benchmark scores are evidence |
| Score JSONs derived from rubric, not hand-typed | ✅ Computed via aggregate_p14.py |

**Results summary**: fixed (mean=63.0) > gnn (58.6) > router (43.2) > single (15.7). Router accuracy 6/15 (40%).

Before claiming a benchmark run is complete:

- [ ] `metadata.json` exists with `run_id`, `timestamp_utc`, `git_sha`, `error_rate`
- [ ] All score JSONs in `scores/` directory
- [ ] `aggregate.json` with mode_summary, win_counts, error_rate_per_mode
- [ ] `checksums.sha256` generated AFTER finalizing all files
- [ ] Error rate reported if any mode > 0%
- [ ] No video/gif evidence required (per this document)
- [ ] Score JSONs are not hand-typed — derived from rubric computation