---
title: "Verify agent-call independence empirically, not from naming/docstrings"
type: source
tags: [worldarchitect.ai, rewards-agent, circuit-breaker, evidence-based-verification, bigquery, root-cause-first]
date: 2026-08-23
source_file: raw/feedback-2026-08-23-verify-agent-call-independence-empirically.md
---

## Summary

While reviewing WorldArchitect.AI PR #9137 (circuit-breaker degradation
design), a review nearly assumed the "rewards" secondary agent
([[RewardsAgent]]) fired as an independent/concurrent Gemini API call
alongside the primary narrative call, based on naming ("secondary agent")
and a docstring literally containing the word "parallel". Investigation via
code read plus a BigQuery join proved it's actually mutually-exclusive
*replacement* routing, not concurrency.

## Key Claims

- `RewardsAgent` **replaces** `StoryModeAgent` for a turn — the agent
  router (`mvp_site/agents.py:4576-4583`) returns `RewardsAgent(game_state)`
  *as the agent for the turn*, not dispatched alongside it.
- `DeferredRewardsAgent`'s own docstring says "Runs IN PARALLEL with story
  mode (**same LLM call**)" — the word "parallel" there describes
  prompt-level injection into one request, not a second concurrent request.
- Empirical proof: a BigQuery join on
  `worldarchitecture-ai.llm_forensics.llm_payloads` by
  `(campaign_id, turn_index)` over a 14-day production window found only 1
  of 161 `RewardsAgent` turns also had a `StoryModeAgent` row at the same
  turn — 160/161 mutual exclusivity.
- `/history` searched 5 sources (Claude Code, Codex, Hermes, agy CLI,
  Cursor) and found **no prior instance** of this exact wrong-conclusion
  pattern in this repo — a first occurrence, not a repeat mistake.

## Key Quotes

> "naming and docstring language ('secondary agent', 'parallel', 'async')
> describe prompt-level/logical structure — multiple concerns handled
> within one LLM call — not transport-level concurrency (two separate API
> requests)"

## Connections

- [[RewardsAgent]] — the entity whose call shape was misjudged
- [[EvidenceBasedVerification]] — the general practice this instantiates:
  verify against structured evidence, not plausible-sounding claims
- [[EmpiricalConcurrencyVerification]] — new concept extracted from this
  source: don't infer call concurrency from naming/docstrings, verify via
  telemetry co-occurrence
- [[worldarchitect.ai]] — the project
- [[Root-Cause-First]] — the review used root-cause code reading, not a
  surface-level docstring read, once the naming assumption was questioned
