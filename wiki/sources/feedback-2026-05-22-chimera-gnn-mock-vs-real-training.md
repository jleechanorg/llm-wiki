---
title: "Chimera GNN Mock Training vs Real Training — 2026-05-22"
type: source
tags: [multi-agent-systems, gnns, training-pipeline, chimera]
date: 2026-05-22
source_file: raw/feedback_2026-05-22_chimera_gnn_mock_vs_real_training.md
---

## Summary

Project Chimera's `train_gnn.py` was discovered to be training the GNN on fabricated hash-based quality scores (`generate_mock_quality_score()`), not actual task execution results. The `gnn_trained.pt` weights were produced from a mock reward signal that had no correlation with real benchmark quality. Fixed by implementing `--real-data` mode that loads actual P14 benchmark quality scores from a JSONL dataset, then retraining the GNN on real signals.

## Key Claims

- `generate_mock_quality_score()` at line 53 of `train_gnn.py` used `base_score = 7.5 + (hash(query) % 30) / 10.0` — deterministic per-query fake scores unrelated to actual output quality
- `run_gnn_mode()` in `run_hard_benchmark.py` does NOT call `GNNTopologyGenerator.generate_topology()` — it uses an LLM call to simulate routing instead
- The P14 benchmark checkpoint at `benchmark_logs/checkpoint.json` contains real 6-dim rubric quality scores that can serve as the training signal
- After real training (`--real-data training_data.jsonl --epochs 10`), GNN mean (4.09) > fixed mean (3.85) in re-benchmark

## Key Quotes

> "In production, this would come from actual task execution results." — comment in `generate_mock_quality_score()`, which was never actually wired to real execution

> "GNN mean=4.09 > fixed mean=3.85 — proves training worked on real signals"

## Connections

- [[GNN]] — the topology learning mechanism that was being trained on fake data
- [[ProjectChimera]] — the parent project this training pipeline belongs to
- [[MultiAgentOrchestration]] — the multi-agent execution this training targets

## Files Changed

| File | Change |
|------|--------|
| `train_gnn.py` | `--real-data` flag, JSONL loader, deprecated mock scorer |
| `collect_training_data.py` | NEW — extracts training data from P14 checkpoint |
| `DESIGN-real-training.md` | NEW — design doc for real wiring |
| `training_data.jsonl` | NEW — 15 (query, topology, quality_score) samples |
| `chimera/gnn_trained.pt` | Retrained on real data |

## Verification

After real training + re-benchmark (15 queries, 3 modes):
- GNN wins vs fixed: 5/15 queries
- GNN mean: 4.09, fixed mean: 3.85
- Training corpus: 15 samples, 10 epochs, Adam optimizer

## Bead

`jleechan-mth` — Chimera real GNN training pipeline