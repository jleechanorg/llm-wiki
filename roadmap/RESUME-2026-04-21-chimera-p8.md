# Resume Prompt — Project Chimera P8 — 2026-04-21

## Context

Project Chimera P8 benchmark is **running in background** on `~/autowiki/`.
Benchmark is at approximately Q6/15 (~2h elapsed of ~6h expected).

## What Was Done

- **P7 ✅**: Rubric redesign committed `7b59ce9` — 6-dim 100pt, Insight heaviest (25pts), 5=floor not ceiling, accuracy gate, 500-char error detection
- **P8 🔄**: Benchmark re-run started 2026-04-21 16:33 local

## How to Resume

### 1. Check benchmark status
```bash
tail -20 ~/autowiki/benchmark_logs/hard_benchmark.log
ps aux | grep run_hard_benchmark | grep -v grep
```

### 2. If COMPLETE: run Phase 3
```bash
cd ~/autowiki
python3 aggregate_benchmark.py
# Check: error rates <5% per mode? Score distribution spans 3+ points?
# If both met: quality comparison is VALID — GNN vs Fixed vs Single answerable
# If not: rubric ceiling still present, more redesign needed
```

### 3. If FAILED: diagnose and restart
```bash
cd ~/autowiki
# Check for RETRY loops or crashes
grep -c "RETRY" benchmark_logs/hard_benchmark.log
# If crashed: kill zombies, restart
pkill -f run_hard_benchmark || true
cd ~/autowiki && nohup python3 run_hard_benchmark.py > benchmark_logs/hard_benchmark.log 2>&1 &
```

### 4. On COMPLETE: commit results
```bash
cd ~/autowiki
# Commit benchmark results
git add benchmark_logs/
git commit -m "chore(chimera): P8 benchmark results $(date +%Y-%m-%d)"
git push

# Update wiki
# wiki/sources/project-chimera-benchmark-hard-queries-2026-04-21.md
# Update: scores per mode, error rates, pairwise results, score distribution
```

### 5. Update roadmap
```bash
cd ~/llm_wiki
# Update nextsteps doc: mark P8 done, record actual results
# Update roadmap/README.md rolling section
# Update wiki/log.md
# Commit and push
```

## Acceptance Criteria

| Metric | Threshold | Notes |
|--------|-----------|-------|
| Error rate | <5% per mode | Single/Fixed/GNN each |
| Score distribution | ≥3pt span across 15 queries | e.g., 5.0–8.0 range |
| Pairwise winners | Discernible GNN vs Fixed vs Single | Not all TIE |

## Key Files

- `~/autowiki/run_hard_benchmark.py` — benchmark runner
- `~/autowiki/aggregate_benchmark.py` — results aggregator
- `~/autowiki/chimera/judge.py` — AI judge with new rubric
- `~/autowiki/benchmark_logs/checkpoint.json` — per-query results
- `~/autowiki/benchmark_logs/hard_benchmark.log` — execution log
- `~/llm_wiki/roadmap/nextsteps-2026-04-21-chimera.md` — full plan

## Memory Files

- `~/.claude/projects/-Users-jleechan-llm-wiki/memory/project_2026-04-21_chimera_p4_run3_complete_rubric_ceiling.md`
- `~/.claude/projects/-Users-jleechan-llm-wiki/memory/feedback_2026-04-21_rubric_design_floor_not_ceiling.md`
- `~/roadmap/learnings-2026-04.md` (search: "rubric ceiling")
