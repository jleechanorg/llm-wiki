# chimera-loop — Autonomous Chimera Benchmark Loop

**Loop interval**: self-paced | **Max duration**: 12h (72 iterations)

## Purpose

Drive Project Chimera P4 hard benchmark to completion, fix harness issues mid-flight, validate evidence, record findings to wiki/beads.

## System Profile

```
SYSTEM_NAME:        Chimera P4 Hard Benchmark
QUALITY_METRIC:     Error rate <5% per mode, valid quality scores for all 15 queries
REPO:               ~/autowiki/
LOG:                benchmark_logs/hard_benchmark.log
CHECKPOINT:         benchmark_logs/checkpoint.json
EVIDENCE_DIR:       benchmark_logs/
BENCHMARK_CMD:      python3 run_hard_benchmark.py (needs MINIMAX_API_KEY env var)
```

## Loop Body (executed on wake + Monitor event)

### Phase 1: OBSERVE

```bash
# Is benchmark running?
ps aux | grep run_hard_benchmark | grep -v grep | awk '{print $2, $10}'

# Log tail (last 20 lines)
tail -20 ~/autowiki/benchmark_logs/hard_benchmark.log

# What query are we on?
grep "QUERY [0-9]*/15" ~/autowiki/benchmark_logs/hard_benchmark.log | tail -1

# Error summary
grep -c "RETRY" ~/autowiki/benchmark_logs/hard_benchmark.log
grep "BENCHMARK COMPLETE" ~/autowiki/benchmark_logs/hard_benchmark.log | tail -1

# Quick evidence check — error rates per mode from checkpoint
cd ~/autowiki && python3 -c "
import json
with open('benchmark_logs/checkpoint.json') as f:
    data = json.load(f)
entries = data.get('results', data) if isinstance(data, dict) else data
modes = ['single', 'fixed', 'gnn']
counts = {m: {'total': 0, 'errors': 0, 'scores': []} for m in modes}
for e in entries:
    for m in modes:
        if m in e.get('modes', {}):
            counts[m]['total'] += 1
            scores = e['modes'][m].get('scores', {})
            if scores.get('error_flag'):
                counts[m]['errors'] += 1
            elif scores.get('overall', 0) > 0:
                counts[m]['scores'].append(scores['overall'])
print(f'Queries complete: {len(entries)}/15')
for m in modes:
    c = counts[m]
    err_rate = c['errors']/c['total']*100 if c['total'] else 0
    avg = sum(c['scores'])/len(c['scores']) if c['scores'] else 0
    print(f'{m}: {c[\"errors\"]}/{c[\"total\"]} errors = {err_rate:.1f}%, avg = {avg:.2f}')
" 2>/dev/null

### Phase 2: DETECT HARNESS FAILURE

Check for these failure patterns and fix immediately:

| Pattern | Detection | Fix |
|---------|----------|-----|
| Benchmark dead | process not running, no COMPLETE in log | Restart benchmark |
| No retry on 529 | 529 in log but no RETRY markers | Add retry to `call_minimax`, restart |
| Checkpoint stale | checkpoint.json older than 5min, benchmark still running | Fix checkpoint write frequency |
| All outputs error | all modes show 0.0 score | Diagnose API issue, may need circuit breaker |
| SHA mismatch | checksum file != actual | Regenerate checksums post-run |

**If COMPLETE detected**: run Phase 3 immediately.

### Phase 3: EVALUATE (on COMPLETE)

```bash
# Run aggregate script
cd ~/autowiki && python3 aggregate_benchmark.py

# Check error rates per mode
grep "error_flag" benchmark_logs/checkpoint.json | python3 -c "
import sys, json
counts = {'single': 0, 'fixed': 0, 'gnn': 0}
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        for mode in counts:
            if d.get('modes', {}).get(mode, {}).get('error_flag'):
                counts[mode] += 1
    except: pass
total = 15
for mode, cnt in counts.items():
    rate = cnt/total*100
    print(f'{mode}: {cnt}/{total} errors = {rate:.1f}%')
"

# Run /er on evidence bundle — invoke evidence-reviewer agent on benchmark_logs/
echo "Running evidence review..."
cd ~/autowiki/benchmark_logs && python3 -c "
import json, os
with open('checkpoint.json') as f:
    data = json.load(f)
entries = data.get('results', data) if isinstance(data, dict) else data
modes = ['single', 'fixed', 'gnn']
counts = {m: {'total': 0, 'errors': 0, 'scores': []} for m in modes}
for e in entries:
    for m in modes:
        if m in e.get('modes', {}):
            counts[m]['total'] += 1
            scores = e['modes'][m].get('scores', {})
            if scores.get('error_flag'):
                counts[m]['errors'] += 1
            elif scores.get('overall', 0) > 0:
                counts[m]['scores'].append(scores['overall'])
print(f'## Evidence Review — {len(entries)}/15 queries')
for m in modes:
    c = counts[m]
    err_rate = c['errors']/c['total']*100 if c['total'] else 0
    avg = sum(c['scores'])/len(c['scores']) if c['scores'] else 0
    print(f'{m}: {c[\"errors\"]}/{c[\"total\"]} errors = {err_rate:.1f}%, valid avg = {avg:.2f}')
" 2>/dev/null
```

### Phase 4: FIX HARNESS (if broken)

If harness issue detected:
1. Kill benchmark process if needed
2. Fix the specific issue in `run_hard_benchmark.py` or `chimera/utils.py`
3. Commit fix: `cd ~/autowiki && git add -A && git commit -m "fix(chimera): <description>"`
4. Restart benchmark
5. Continue loop

### Phase 5: RECORD

```bash
# Append cycle findings to ~/roadmap/evolve-loop-findings.md
echo "## Chimera P4 Cycle — $(date +%Y-%m-%d_%H:%M)" >> ~/roadmap/evolve-loop-findings.md
echo "- Query progress: $(grep 'QUERY' benchmark_logs/hard_benchmark.log | tail -1)" >> ~/roadmap/evolve-loop-findings.md
echo "- Error count: $(grep -c RETRY benchmark_logs/hard_benchmark.log)" >> ~/roadmap/evolve-loop-findings.md
echo "- Harness fixes: <list>" >> ~/roadmap/evolve-loop-findings.md

# Commit
cd ~/autowiki && git add benchmark_logs/ && git commit -m "chore(chimera): log cycle $(date +%Y-%m-%d_%H:%M)" 2>/dev/null || true
```

### Phase 6: UPDATE WIKI (on COMPLETE)

```bash
# Update benchmark wiki page with actual results
# ~/llm_wiki/wiki/sources/project-chimera-benchmark-hard-queries-2026-04-21.md

# Run /wiki-ingest to update entities/concepts if new findings

# Create bead for completed
br create "Chimera P4 complete — $(date)" --type task --priority 3
```

### Phase 7: RECAP

```
## Chimera-Loop Cycle — HH:MM
- Progress: Q{n}/15 completed
- Error rate: X% (target <5%)
- Retries: N total
- Harness fixes: N applied this cycle
- Next action: <what happens next>
```

## Monitor Armed

On loop start, arm a persistent Monitor on `~/autowiki/benchmark_logs/hard_benchmark.log` watching for:
- `BENCHMARK COMPLETE` → wake for Phase 3
- `BENCHMARK FAIL` → wake for Phase 4 (harness fix)
- `RETRY attempt 3/3 failed` → wake for Phase 4 (stuck retry)
- `QUERY [0-9]+/15` → informational only, don't wake

## Invocation

```bash
/chimera-loop          # Start the loop (self-paced, monitor-driven)
/chimera-loop --status  # Show current benchmark status without restarting
/chimera-loop --stop   # Stop the loop gracefully
```

## Key Files

- `~/autowiki/run_hard_benchmark.py` — benchmark runner (must have retry logic)
- `~/autowiki/aggregate_benchmark.py` — result aggregation script
- `~/autowiki/benchmark_logs/checkpoint.json` — per-query results
- `~/autowiki/benchmark_logs/hard_benchmark.log` — execution log
- `~/roadmap/evolve-loop-findings.md` — cycle log

## Anti-Stall Rules

- Process dead + no COMPLETE → restart benchmark
- 3 consecutive cycles same query → check for hang, may need to kill and restart
- RETRY loop stuck (>10 retries same call) → circuit breaker trip detected, wait before retry
- SHA mismatch on COMPLETE → regenerate before declaring done
- If benchmark fails 3x consecutively → open bead, stop loop, alert user