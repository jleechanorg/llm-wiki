---
name: verify-agent-call-independence-empirically
description: "Don't infer whether two agent/LLM calls are concurrent vs. mutually-exclusive from naming or docstrings (\"secondary\", \"async\", \"parallel\") — verify empirically against production telemetry before treating independence as a load-bearing review assumption."
metadata: 
  node_type: memory
  type: feedback
  bead: rev-l923i
  originSessionId: 61376ccd-8e06-4e23-a9e2-70198a4748b7
  modified: 2026-08-23T21:15:09.113Z
---

While reviewing PR #9137 (WorldArchitect.AI circuit-breaker degradation
design), a review nearly assumed the "rewards" secondary agent
(`RewardsAgent`) fired as an **independent/concurrent Gemini API call**
alongside the primary narrative call — based on the naming ("secondary
agent") and a docstring on `DeferredRewardsAgent` that literally contained
the word "parallel".

**What actually happens:** `RewardsAgent` *replaces* `StoryModeAgent` for a
turn — mutually-exclusive routing, not a second concurrent call. The one
docstring that said "parallel" meant "prompt-injected into the SAME LLM
call," not a second independent request. Confirmed two ways:

1. **Code**: the agent router (`mvp_site/agents.py:4576-4583`,
   `:4741-4755`, `:4282-4294`) returns `RewardsAgent(game_state)` *as the
   agent for the turn*, not dispatched alongside `StoryModeAgent`.
2. **BigQuery** (`worldarchitecture-ai.llm_forensics.llm_payloads`, real
   prod, 14-day window): joined all `agent="RewardsAgent"` turns back to
   themselves by `(campaign_id, turn_index)` — of 161 RewardsAgent rows,
   only 1 also had a `StoryModeAgent` row at the same turn. 160/161 mutual
   exclusivity.

**Root cause of the near-miss:** naming and docstring language ("secondary
agent", "parallel", "async") describe *prompt-level/logical* structure —
multiple concerns handled within one LLM call — not *transport-level*
concurrency (two separate API requests). Code-reading and docstrings alone
could not disambiguate this; only the empirical BQ row-co-occurrence check
settled it definitively.

**Rule going forward:** when a design or review verdict depends on whether
two agent/LLM calls are concurrent vs. sequential/mutually-exclusive, don't
infer it from naming or docstring language containing words like "async",
"parallel", or "secondary". Verify empirically against real telemetry —
join production rows by `(campaign_id, turn_index)` (or the equivalent
request-ID/timestamp key for other systems) and check for genuine
co-occurrence — before treating independence as a given, especially when
it's load-bearing for a review verdict or architectural decision.

**Provenance note:** `/history` searched across 5 sources (Claude Code,
Codex, Hermes, agy CLI, Cursor) and found **no prior instance** of this
exact wrong-conclusion pattern in this repo — this is a first occurrence,
not a repeat mistake, though a related (but distinct) `RewardsAgent`
routing investigation exists at
[[project_2026-08-18_time_travel_rewardsagent_root_cause]] from an
unrelated campaign time-travel bug.

**Implication for PR #9137**: the circuit-breaker degradation design's
actual premise ("if a turn routed to a secondary-agent MODE trips the
breaker, degrade gracefully") still holds — each turn makes exactly one
LLM call, so there's no scenario of a concurrent rewards call silently
failing. One loose thread flagged separately (bead `rev-oyjx5`):
`DeferredRewardsAgent` injects rewards content into the *same*
`StoryModeAgent` call but hardcodes `agent_mode=MODE_REWARDS`, which could
mis-key the degrade-vs-hard-fail branch for what's really a primary
narrative turn.
