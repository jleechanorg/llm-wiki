---
title: "Empirical Concurrency Verification"
type: concept
tags: [concurrency, verification, evidence-based, bigquery, agent-architecture]
sources: [feedback-2026-08-23-verify-agent-call-independence-empirically]
last_updated: 2026-08-23
---

## Summary

When a design or review claim depends on whether two agent/LLM calls are
concurrent vs. sequential/mutually-exclusive, naming and docstring language
("secondary agent", "async", "parallel") are unreliable signals — they
often describe prompt-level/logical structure (multiple concerns handled
within one LLM call) rather than transport-level concurrency (two separate
API requests). Code-reading and docstrings alone cannot always
disambiguate this.

## Key Claims

- The definitive test is empirical: join production telemetry rows by a
  shared correlation key (e.g. `(campaign_id, turn_index)` for
  WorldArchitect.AI's BigQuery `llm_payloads` table, or the equivalent
  request-ID/timestamp key for other systems) and check for genuine
  co-occurrence of the two supposedly-concurrent calls.
- A single docstring or variable name containing "parallel"/"async" is not
  sufficient evidence of transport-level concurrency — verify the actual
  dispatch/routing code AND the production data before treating
  independence as a load-bearing assumption.

## Example (source case)

[[RewardsAgent]] in WorldArchitect.AI was assumed to be an independent
concurrent Gemini call based on its "secondary agent" naming and a
docstring saying "parallel". A BigQuery join by `(campaign_id, turn_index)`
showed 160/161 mutual exclusivity with the primary narrative agent —
proving it's replacement routing, not concurrency. See
[[feedback-2026-08-23-verify-agent-call-independence-empirically]].

## Connections

- [[EvidenceBasedVerification]] — the general practice this specializes
- [[Concurrency]] — the systems-level concept this concept disambiguates
  from prompt-level parallelism
- [[RewardsAgent]] — the entity involved in the source case
- [[worldarchitect.ai]]
