---
title: "LLM-behavior bugs need direct ablation, not research fan-out"
type: source
tags: [debugging, gemini, worldarchitect, methodology, root-cause-first]
date: 2026-08-16
source_file: raw/feedback_2026-08-16_llm_bug_root_cause_needs_direct_ablation_not_research_fanout.md
---

## Summary

WorldArchitect.AI's `gemini-3.7-flash` (and `gemini-3.6-flash`) enters a runaway
`code_execution` tool-call loop — `FinishReason.TOO_MANY_TOOL_CALLS` after
~240-270 internal iterations, 55s+ latency, tens of millions of cached tokens per
turn — while `gemini-3-flash-preview` does not. A full round of `/research` +
`/advice` (Opus subagent + 4-model `/secondo` panel) + `/web-advice` (real Grok
and Perplexity browser sessions) produced useful external context but never
found the actual trigger, and one model in the panel fabricated a false "256
internal calls" ceiling that had to be refuted by two other independent models.
The agent then began writing a client-side circuit-breaker workaround directly
into production code before the user stopped it and redirected to a controlled
ablation experiment against the real API instead. A ~30-line standalone script
found the exact trigger in minutes: the loop is caused by combining the
`code_execution` tool with a bare `response_mime_type="application/json"` (no
schema); adding an explicit `response_json_schema` fixed it 10/10 runs.

## Key Claims

- **Correction (same day):** this page originally called the trigger
  "undocumented." The user challenged that directly and a follow-up web search
  found Google's own AI Developers Forum has a real thread ("Infinite looping
  Thinking steps for Gemini 3 APIs") describing the same failure class — Gemini
  3 + JSON output getting stuck looping/validating instead of terminating — via
  a different mechanism (the thinking block, not repeated `code_execution` tool
  calls) and without naming `response_json_schema` as a fix. The *exact*
  mechanism (code_execution specifically, fixed by response_json_schema
  specifically) is still unconfirmed by any Google doc found, but the *failure
  class* has independent prior art. Lesson: verify a negative claim
  ("nothing is documented") with an actual search before asserting it, not just
  by summarizing what a prior research pass already returned.
- Fine-grained interactions between two SDK config fields on specific model
  versions are hard to find via external research/multi-model synthesis tools
  when the research query is scoped too narrowly (ours searched
  `TOO_MANY_TOOL_CALLS` + `code_execution` and missed a differently-worded
  thread) — those tools are upper-bounded by what has been written down AND by
  how well the query matches how it was written down.
- When direct API/SDK access exists and a minimal reproduction is cheap (seconds,
  pennies per call), building a live ablation script is the correct *first* move
  for a live LLM-behavior bug — this is [[Systematic Debugging (Phase 1: Build a Feedback Loop)]] Phase 1 ("build a
  feedback loop") applied literally to a model-behavior regression rather than a
  code regression.
- [[Root-Cause-First]] discipline should block writing a defensive/protective patch
  (circuit breaker, retry, rollback/exclusion) before the actual trigger is
  isolated — a fix for an unknown cause is a guess, not a fix.
- Research and multi-model second-opinion fan-outs are not wasted work — the SDK
  version/enum history and forum corroboration found by `/research` were genuinely
  useful and got folded into the bead — but they are context gathered in parallel
  with or after ablation, never a substitute for it when reproduction is cheap.
- A merged PR (#8951) claimed to fix this exact bug via a prompt-guardrail change
  that had already been empirically disproven (3/3 runaway reproductions with
  that exact instruction text), backed by only 3 test samples against a real-world
  ~3.3% failure rate — a sample size with a ~90% chance of a false-clean result
  even if the bug were fully unfixed. Same evidence-thinness pattern as prior
  fabricated-evidence incidents in this project.

## Key Quotes

> "another agent is coding and stop these fucking workarounds figure out root
> cause and use ablation. can gemini execute 2+2? with 3.7 flash. if so then
> gradually make it more compocated until it approaches our actual code and see
> where it goes wrong dont code mvp site code yet" — the user, redirecting the
> agent from a defensive patch to a root-cause ablation experiment

## Connections

- [[Gemini]] — the model family exhibiting this behavior
- [[GeminiAPI]] — the `code_execution` built-in tool and `response_mime_type`/
  `response_json_schema` config surface where the bug lives
- [[GeminiProvider]] — the WorldArchitect.AI module (`gemini_provider.py`) that
  would carry the fix
- [[WorldArchitectAI]] — the project this investigation happened in
- [[Root-Cause-First]] — the discipline that should have preempted the
  circuit-breaker patch attempt
- [[Systematic Debugging (Phase 1: Build a Feedback Loop)]] — Phase 1 (build a feedback loop) is the generalizable
  method this incident validates
