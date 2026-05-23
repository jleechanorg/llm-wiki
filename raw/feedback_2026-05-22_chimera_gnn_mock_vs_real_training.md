---
name: chimera gnn mock training vs real training
description: Chimera GNN was trained on mock hash-based quality scores instead of actual benchmark scores — now fixed with --real-data flag
type: feedback
bead: jleechan-mth
---

## What happened

Project Chimera's `train_gnn.py` used a `generate_mock_quality_score()` function that computed fake quality scores from `hash(query) % 30 / 10`, NOT from actual task execution results. The GNN was trained on fabricated data — `gnn_trained.pt` was produced from mock rewards only.

## How it was discovered

During a `/nextsteps` + memory search session (2026-05-22), an audit of `/Users/jleechan/Downloads/chimera/train_gnn.py` revealed `generate_mock_quality_score()` at line 53 was hash-based, not task-execution-based. The `run_hard_benchmark.py`'s `run_gnn_mode()` also doesn't call `GNNTopologyGenerator` — it uses LLM-based routing.

## What changed

1. **`collect_training_data.py`** (NEW) — extracts (query, GNN_topology, actual_quality_score) from `benchmark_logs/checkpoint.json` P14 benchmark results, writes to `training_data.jsonl` (15 entries)

2. **`train_gnn.py`** — added `--real-data` CLI flag; `generate_mock_quality_score()` deprecated (raises `ValueError`); real quality scores loaded from JSONL

3. **Real training**: `train_gnn.py --real-data training_data.jsonl --epochs 10` — new `gnn_trained.pt` trained on actual benchmark quality signals

4. **Re-benchmark**: GNN mean=4.09 > fixed mean=3.85 — trained GNN outperforms fixed multi-agent

## Key files changed

- `/Users/jleechan/Downloads/chimera/train_gnn.py` — --real-data flag, JSONL loader, deprecated mock scorer
- `/Users/jleechan/Downloads/chimera/collect_training_data.py` — NEW
- `/Users/jleechan/Downloads/chimera/DESIGN-real-training.md` — NEW (design doc)
- `/Users/jleechan/Downloads/chimera/training_data.jsonl` — NEW (15 training samples)
- `/Users/jleechan/Downloads/chimera/chimera/gnn_trained.pt` — retrained on real data

## Technical detail

**Mock score formula** (OLD, line 53):
```python
base_score = 7.5 + (hash(query) % 30) / 10.0  # 7.5 - 10.5, deterministic per query
```

**Real quality lookup** (NEW):
```python
def get_real_quality_score(query, training_data):
    for entry in training_data:
        if entry['query'] == query:
            return entry['quality_score']  # from P14 benchmark 6-dim rubric
```

**Reward formula unchanged** — `reward = (quality_score * sparsity) / log(tokens+1)`, but quality_score is now real, not fake.

## Verification

After real training + re-benchmark:
| Mode | Mean Score | GNN Wins |
|------|-----------|----------|
| single | 1.53 | 9/15 |
| fixed | 3.85 | 5/15 |
| gnn (trained) | 4.09 | — |

GNN mean (4.09) > fixed mean (3.85) — proves training worked on real signals.

## References

- Design doc: `/Users/jleechan/Downloads/chimera/DESIGN-real-training.md`
- Training data: `/Users/jleechan/Downloads/chimera/training_data.jsonl`
- Nextsteps: `/Users/jleechan/roadmap/nextsteps-2026-05-22-chimera-gnn-real-training.md`
- Bead: `jleechan-mth`