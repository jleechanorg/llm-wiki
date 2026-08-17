---
title: "Root-Cause-First"
type: concept
tags: [debugging, methodology, engineering-discipline]
date: 2026-08-16
---

## Definition

A rule that fixes for bugs must address the underlying cause before any backend
protection, fallback, clamp, sanitizer, retry, suppression, or guardrail logic is
added. If a bug tempts a defensive patch, that temptation is the signal to stop
and inspect raw inputs/outputs (model prompts/responses, request configs, logs)
first — the protective code goes in only after the root cause is understood, if
it's still needed at all.

## Why it matters

Defensive patches written before the root cause is known tend to treat the
symptom, not the disease: they can mask the bug (making it harder to find later),
address the wrong trigger, or add permanent complexity for a problem that a
one-line config change would have solved. In the case documented in
[[LLM-behavior bugs need direct ablation, not research fan-out]], an agent started writing a client-side
circuit-breaker into production code for a Gemini API runaway-loop bug before
the actual trigger (a missing `response_json_schema`) was known — the patch
would have shipped as permanent scaffolding around a problem that had a much
smaller, more precise real fix.

## Connections

- [[Systematic Debugging (Phase 1: Build a Feedback Loop)]] — root-cause-first is the "why" behind Phase 1's
  insistence on a real reproduction before hypothesizing fixes
- [[LLM-behavior bugs need direct ablation, not research fan-out]] — a concrete incident where skipping
  this discipline nearly shipped a workaround instead of a fix
- [[WorldArchitectAI]] — the project whose CLAUDE.md/AGENTS.md codify this rule
