---
title: "Experience Replay"
type: concept
tags: [experience-replay, reinforcement-learning, RL, memory, meta-harness]
sources: [meta-harness-paper]
last_updated: 2026-04-14
---

## Summary

Experience replay is a technique from reinforcement learning where the agent stores past experiences (state, action, reward, next state) and samples from this replay buffer to learn. Meta-Harness applies an analogous concept through filesystem-based history — storing all prior candidates (source code, scores, execution traces) and referencing them during optimization.

## Key Claims

- Experience replay enables learning from diverse past experiences
- Meta-Harness stores prior candidates as files for selective replay
- The agentic proposer references 20+ prior candidates per step
- Filesystem operations (grep/cat) enable selective experience retrieval
- Full fidelity storage (code + traces + scores) enables rich replay

## Experience Replay vs Filesystem History

| Aspect | Traditional Experience Replay | Meta-Harness Filesystem History |
|--------|------------------------------|--------------------------------|
| What is stored | State-action-reward tuples | Full source, scores, traces |
| Retrieval | Random/batch sampling | Selective grep/cat queries |
| Prior candidates | Limited buffer | 20+ per iteration |
| Fidelity | Compressed | Full |

## Connections

- [[FilesystemHistory]] — Meta-Harness implements experience replay for code
- [[FeedbackLoop]] — experience replay enables improved feedback
- [[AgenticProposer]] — uses experience replay to make decisions
- [[MetaHarness]] — implements experience replay at scale
- [[SelfImproving]] — experience replay enables self-improvement
