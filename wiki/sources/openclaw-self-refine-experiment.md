---
title: "OpenClaw Self-Refine Experiment — Cycle 1"
type: source
tags: [openclaw, self-refine, self-critique, jleechanclaw, experiment]
date: 2026-04-14
source_file: ~/.openclaw/papers/experiment_self_refine/
---

## Summary

Cycle 1 of the Self-Refine experiment tested whether structured self-critique + revision loops (Madaan et al., NeurIPS 2023) improve jleechanclaw PR generation on TEST-PR-001 (staging require-mention fix). **Result: ABANDONED for deterministic fixes. Context > Self-Critique.**

## Key Claims

- Self-refine HIT TOKEN CAP before converging on TEST-PR-001 — 4,096 tokens, 45s — worse than baseline (2,221 tokens, ~5s)
- Root cause: neither prompt provided actual file content — self-critique cannot compensate for missing context
- Key insight: **Context > Self-Critique** for this class of PR
- Pivot decision: test self-refine on ambiguous complex tasks (TEST-PR-008, TEST-PR-009) WITH context provided

## Ground Truth (TEST-PR-001)

```python
# The actual fix (3-line Python snippet inside bash):
slack_channels = staging_cfg.get("channels", {}).get("slack", {}).get("channels", {})
for ch in slack_channels:
    slack_channels[ch]["requireMention"] = True
```

Neither baseline nor self-refine produced this — both missed the Python-in-bash architecture.

## Baseline vs Self-Refine Results

| Metric | Baseline | Self-Refine |
|--------|----------|-------------|
| Architecture match | Wrong (bash vs Python-in-bash) | Wrong (over-engineered generator) |
| Correct logic | No | No |
| Test architecture | Wrong (YAML vs pytest fixture) | Partial |
| Token usage | 2,221 out | 4,096 out (hit cap) |
| Time to result | ~5s | ~45s |

## When Self-Refine Helps

**Self-refine helps when:**
1. Model has sufficient context (file content provided)
2. Task has ambiguous requirements (self-critique resolves ambiguity)
3. Edge cases are non-obvious (self-critique surfaces them)

**Self-refine does NOT help when:**
1. Model lacks actual file content (this experiment)
2. Fix is deterministic and context-dependent (configuration changes)
3. Token budget is constrained (self-refine doubles token usage)

## Next Steps (Pivoted)

- Iteration 2: Same TEST-PR-001 but WITH actual file content provided in prompt
- Hypothesis: context was the real variable, not self-critique
- Future: test on ambiguous complex tasks (TEST-PR-008, TEST-PR-009) WITH context

## Connections

- [[SelfCritiqueVerificationLoop]] — 3-iteration cap, phases 0-3
- [[SelfRefinement]] — Madaan et al. 2023 technique
- [[jleechanclaw-openclaw-notifier]] — relevant PR context
