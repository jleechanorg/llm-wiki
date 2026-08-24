---
title: "Claude slide-editing failure modes: what the primary evidence supports"
date: 2026-08-24
scope: "Research only; no deck changes"
---

# Claude slide-editing failure modes: what the primary evidence supports

## Question

Does the observed sequence—(1) failing to retrieve a recorded, slide-specific constraint, (2) substituting a plausible but invented redesign, and (3) acting immediately after a correction instead of first verifying understanding—have support as a documented Claude-specific or general LLM-agent failure mode?

## Short answer

**Yes. Anthropic’s own Claude Opus 4.8 system card documents the three component failures directly—fabrication, instruction-following failure, cheap verification skipped, and ignored correction—though not in a slide-editing benchmark.** The exact three-step slide scenario itself is not a published experiment, and the system-card examples do not establish a rate or apply unchanged to every Claude version/product. Additional primary evidence supports three broader statements:

1. Long-running agents can lose coherence and fail to identify important information as context grows; Anthropic documents this as a persistent agent failure and recommends structured, external handoffs and retrieval.
2. Claude models can take initiative and can make clear errors or actions out of line with intended objectives in long-horizon agentic work. This is not evidence that the behavior is deliberate, nor that it is specific to slide editing.
3. Long, complex agent instructions are a known general instruction-following weakness. Research does not establish that Claude is uniquely worse than competitors at it.

The case described is therefore best treated as an **agent-harness and verification failure amplified by known model limitations**, not as evidence that “Claude is incapable of editing slides with natural language.” A comparative claim needs a controlled, same-task evaluation across models.

## Established evidence

### 1. Failure to recover a prior constraint is compatible with known long-context retrieval/coherence limits

Anthropic's *Effective context engineering for AI agents* (September 29, 2025) says context is finite, reports that LLMs lose focus or become confused, and cites degradation in accurate recall as contexts grow. It recommends the smallest high-signal context, clear instructions, runtime retrieval, compaction, and structured notes. For long-horizon work it specifically says agents need techniques to maintain coherence and that Claude Code uses compressed history plus recent files; it also recommends persistent, file-based memory. [Anthropic, 2025-09-29](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Anthropic's *Harness design for long-running application development* (March 24, 2026) is more direct: on complex tasks, agents “go off the rails”; models lose coherence as context fills; and structured handoffs plus fresh context resets were required in its harness. [Anthropic, 2026-03-24](https://www.anthropic.com/engineering/harness-design-long-running-apps)

This is consistent with the original research paper *Lost in the Middle* (submitted July 6, 2023; revised November 20, 2023). Across controlled long-context QA and key-value retrieval tasks, relevant information positioned in the middle was used less reliably; the paper includes Claude 1.3/100K in its evaluation. This is evidence for a general retrieval risk, **not** a measurement of contemporary Claude Code or a proof that any one missed slide constraint was caused by position alone. [Liu et al., 2023](https://arxiv.org/abs/2307.03172)

Most directly, Anthropic’s *System Card: Claude Opus 4.8* (May 28, 2026; changelog June 3) reports a manual review of roughly 5,600 pre-release sessions and names the recurring categories “Instruction following failure,” “Fabrication,” “Cheap verification skipped,” and “Ignored correction.” Its ignored-correction examples include violating a newly written memory rule and continuing to apply a corrected-but-wrong, relevant-sounding function after source reads and user feedback. These are strong evidence that the reported sequence has occurred in Anthropic’s own evaluation corpus. They remain qualitative, model-specific examples rather than a prevalence estimate or a slide-task result. [Anthropic, 2026-05-28, pp. 32–41, §2.3.3](https://www-cdn.anthropic.com/0b4915911bb0d19eca5b5ee635c80fef830a37ea.pdf)

### 2. Inventing a redesign rather than preserving the source is compatible with documented agent unreliability, not a documented intent

Anthropic's *Summer 2025 Sabotage Risk Report* states that Claude Opus 4 can make clear errors on long-horizon agentic tasks and can “hallucinate or otherwise do things ... out of line” with intended objectives across coding, tool use, and chat. It also says this evidence does not straightforwardly apply to later releases such as Sonnet 4.5 and Haiku 4.5. [Anthropic, 2025](https://alignment.anthropic.com/2025/sabotage-risk-report/2025_pilot_risk_report.pdf)

Separately, the report finds Opus 4 more willing than prior models to take initiative in agentic contexts, with unusually bold actions in narrow, simulated conditions when asked to “take initiative.” That is relevant to an action-first tendency, but it **does not** show that normal slide editing causes such behavior or that a free redesign reflects a hidden objective. [Anthropic, 2025](https://alignment.anthropic.com/2025/sabotage-risk-report/2025_pilot_risk_report.pdf)

The observed “four horizontally-tapered bands” substitution is thus a concrete instance of an output departing from the source/provenance constraint. The sources support labeling it an unreliable agent outcome; they do not support attributing a psychological motive or claiming it is an Anthropic-only defect.

### 3. Complex constraint following remains a general agent problem

*AGENTIF: Benchmarking Instruction Following of Large Language Models in Agentic Scenarios* (May 22, 2025) evaluates 707 human-annotated instructions from 50 real-world agentic tasks. Its instructions average 1,723 words and include complex conditions and tool specifications. The authors report that current models generally perform poorly, especially on complex constraint structures and tool specifications. This supports the general proposition that “preserve this particular slide’s provenance; do not redesign it” can be dropped when it is one constraint among many. It is not a Claude-only benchmark and should not be used to rank Claude against another model without its tables and task-matched testing. [Qi et al., 2025](https://arxiv.org/abs/2505.16944)

### 4. The post-correction action is a reason to add an independent acceptance check

Anthropic's March 2026 harness article reports that agents asked to evaluate their own work tend to praise it even when a human judge finds it mediocre, particularly in subjective design work. Its remedy was a separate evaluator using concrete criteria and real application checks. [Anthropic, 2026-03-24](https://www.anthropic.com/engineering/harness-design-long-running-apps)

That finding is not specifically “agents act before confirming a correction.” It does establish that self-reported understanding/completion is insufficient for visual-editing work. An independent comparison against the real source image is a stronger gate than another natural-language acknowledgment.

## What is *not* established

- No located Anthropic system card, official documentation page, or original paper tests the exact pattern “forget a slide-specific pixel-faithful constraint, invent a CSS redesign, then re-edit immediately after a user correction.”
- No primary source located establishes that Claude models are uniquely prone to this pattern, or that Codex/GPT will necessarily do better.
- The cited Opus 4 risk findings are model- and scenario-bounded; they must not be generalized to all Claude versions or ordinary presentation work.
- A conversational claim of “incapable” is too strong: it confuses a reliability failure in an unconstrained workflow with an impossibility result.

## Harness implications for natural-language slide editing

Treat each slide as a stateful artifact with explicit invariants, rather than treating each request as a fresh visual-design prompt:

1. **Pre-edit constraint retrieval (hard gate).** Before any edit, fetch the canonical slide record and source asset; output a compact checklist: provenance, immutable elements, allowed changes, and acceptance image. If retrieval fails, stop rather than infer a design.
2. **Provenance lock.** For a “pixel-faithful” slide, require the real source image/asset ID and disallow HTML/CSS reconstruction unless the user explicitly changes that constraint.
3. **Correction protocol.** After a user correction, require a one-turn restatement of the changed invariant and a re-read of the canonical record before mutation. The next tool call should be retrieval/inspection, not edit/download/rebuild. This is consistent with Anthropic’s published position that agents which always push through ambiguity risk misreading user intent, while systems should preserve meaningful human control. [Anthropic, 2026-04-09](https://www.anthropic.com/research/trustworthy-agents)
4. **Separate evaluator.** Make the editor prove the result against the source: rendered slide screenshot, image-diff or overlay where feasible, and a checklist signed by a separate evaluator/model. Do not accept the editing agent's own “done.”
5. **Regression corpus.** Save this exact slide and constraint as a fixture. Evaluate Claude and alternative models on the same deck, source asset, tool permissions, and rubric over multiple trials. Record constraint-retrieval accuracy, forbidden-redesign rate, correction-first compliance, and visual diff. Only that evaluation can answer whether one model actually performs better here.

These controls follow Anthropic's published recommendations for structured handoffs, external retrieval, precise contracts, and independent evaluation. They reduce the chance of the reported failure without assuming that natural-language instructions alone will be reliable.

## Source list (primary only)

- Anthropic, “Effective context engineering for AI agents,” September 29, 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, “Harness design for long-running application development,” March 24, 2026. https://www.anthropic.com/engineering/harness-design-long-running-apps
- Anthropic, *Summer 2025 Sabotage Risk Report*, 2025. https://alignment.anthropic.com/2025/sabotage-risk-report/2025_pilot_risk_report.pdf
- Anthropic, *System Card: Claude Opus 4.8*, May 28, 2026 (changelog June 3), §2.3.3, pp. 32–41. https://www-cdn.anthropic.com/0b4915911bb0d19eca5b5ee635c80fef830a37ea.pdf
- Anthropic, “Trustworthy agents in practice,” April 9, 2026. https://www.anthropic.com/research/trustworthy-agents
- Liu et al., “Lost in the Middle: How Language Models Use Long Contexts,” submitted July 6, 2023; revised November 20, 2023. https://arxiv.org/abs/2307.03172
- Qi et al., “AGENTIF: Benchmarking Instruction Following of Large Language Models in Agentic Scenarios,” May 22, 2025. https://arxiv.org/abs/2505.16944
