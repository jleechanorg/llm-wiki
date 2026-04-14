---
title: "Meta-Harness: End-to-End Optimization of Model Harnesses"
type: source
tags: [meta-harness, harness-engineering, outer-loop-optimization, context-management, agentic-proposer, automated-harness]
date: 2026-04-14
source_file: arxiv.org/abs/2603.28052
---

## Summary

Meta-Harness is an outer-loop system that searches over harness code for LLM applications. Unlike prior text optimizers that compress feedback to short templates/summaries, Meta-Harness uses an agentic proposer that accesses full source code, execution traces, and scores through a filesystem. Key results: 7.7 point improvement on text classification with 4x fewer tokens, 4.7 point improvement on 200 IMO problems, #1 on TerminalBench-2 among Haiku 4.5 agents.

**Paper:** arxiv.org/abs/2603.28052
**Authors:** Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, Chelsea Finn (Stanford/MIT/KRAFTON)

## Key Claims

### The Harness Problem
- Changing the harness around a fixed LLM produces a **6x performance gap** on the same benchmark (Tian2026)
- Harness = code that determines what information to store, retrieve, and present to the model
- Harness engineering remains largely manual despite its importance

### Why Prior Text Optimizers Fail for Harness Engineering
| Limitation | Description |
|---|---|
| Memoryless | Condition only on current candidate |
| Scalar scores only | Rely primarily on scalar scores |
| Compressed feedback | Restrict feedback to short templates or LLM summaries |
| Short context | 100-30,000 tokens per optimization step vs 10M tokens for harness search |

### Meta-Harness Architecture
1. **Agentic Proposer** — coding agent that reads source code, invokes tools, modifies code
2. **Filesystem-based History** — full history of prior candidates stored as files (source code, scores, execution traces)
3. **Standard ops** — proposer uses `grep` and `cat` rather than ingesting all context as prompt
4. **Selective diagnosis** — reads median **82 files per iteration**, references 20+ prior candidates per step
5. **10,000,000 tokens** per evaluation (vs 30K max in prior text optimizers)

### Key Results
| Task | Result |
|------|--------|
| Online text classification | +7.7 points over ACE, 4x fewer tokens |
| Retrieval-augmented math (200 IMO) | +4.7 points avg across 5 models |
| TerminalBench-2 coding | #1 among all Claude Haiku 4.5 agents, surpasses Terminus-KIRA |

### The Core Insight
> "Richer access to prior experience can enable automated harness engineering."

Full source code + execution traces + scores through filesystem >> compressed summaries.

## Connections

- [[HarnessEngineering]] — the practice of refining code around an LLM (this paper defines the field)
- [[AdaptiveContextTruncation]] — contrast: this paper optimizes WHAT to present; truncation just makes it fit
- [[ContextCompaction]] — related: both manage context, but Meta-Harness searches over the compaction strategy itself
- [[ContextManagement]] — harness IS the context management code
- [[OuterLoop]] — outer-loop vs inner-loop distinction
- [[AgenticProposer]] — the coding agent that searches harness space
- [[MemoryAugmentedLLM]] — adaptive retrieval is mentioned as related (MemGPT, RecursiveLM)
- [[ContextWindowManagement]] — what Meta-Harness optimizes
- [[TerminalBench]] — the agentic coding benchmark where it ranked #1
