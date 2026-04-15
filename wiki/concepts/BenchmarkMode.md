---
title: "Benchmark Mode"
type: concept
tags: [benchmark-mode, prediction, technique-evaluation]
sources: [pr-recreate-pipeline]
last_updated: 2026-04-15
---

## Summary

Benchmark Mode is the **wrong** approach for auto-research — it predicts what already-merged PRs would do, scores prediction accuracy, but produces zero real code changes. Contrast with [[PRRecreatePipeline]] which actually fixes from pre-state.

## Why Benchmark Mode Is Wrong

The current auto-research system (Cycles 1-26) ran in benchmark mode:
- Given a PR description → predict what the diff would look like
- Compare prediction vs actual merged diff
- Score: prediction accuracy + 6-dim rubric

**Problem**: Measures how well an agent can predict history. Doesn't produce any real code.

## Symptoms of Benchmark Mode

- All results are in `test-prs/[autoresearch]-pr{NUMBER}-selfrefine-test.md`
- No actual code changes in worldarchitect.ai
- No real PRs opened
- Agent says "predict" rather than "fix"
- Scoring is against historical diffs, not against open issues

## Contrast with [[PRRecreatePipeline]]

| | Benchmark Mode | Recreate Mode |
|--|---------------|---------------|
| Target | Historical PRs | Historical PRs OR open issues |
| Output | Prediction | Real code |
| Can open PR? | No | Yes (if delta > 0) |
| Value | Measuring technique accuracy | Actually fixing bugs |
| Token cost | Same | Same |

## How to Escape Benchmark Mode

1. Never predict — always implement
2. If there's no open issue to fix, create one first
3. The goal is real PRs, not good predictions
