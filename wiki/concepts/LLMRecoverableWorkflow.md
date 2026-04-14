---
title: "LLM Recoverable Workflow"
type: concept
tags: [pairv2, recovery, architecture]
sources: []
last_updated: 2026-02-24
---

## Definition

An LLM Recoverable Workflow is an AI agent execution pattern where the orchestrating system delegates all semantic judgment to the model and never uses heuristics, timing gates, or exact-match checks to override the model's verdict. When the model says something is wrong, the system responds by giving the model the feedback and a chance to fix it, rather than falling back to a human.

## Core Tenets

1. **Trust model verdicts** — If the verifier says FAIL, trust the verdict. Never override it with a timing heuristic or path-existence check.
2. **Process exit as primary signal** — A tmux session going dead means the agent is done. Signal files (IMPLEMENTATION_READY) are optional best-effort hints, not completion gates.
3. **Continue on missing files** — Missing user-provided contract files or design docs are brittle operational issues, not evidence of invalid implementation. Fall back to LLM generation.
4. **Hard validation becomes soft warnings** — Schema validation failures, missing artifact paths, and field name typos should be logged as warnings, not gating conditions that prevent the verifier from running.

## Pattern: Hard-Fail vs Soft-Warn

| Pattern | Hard-Fail (Anti-pattern) | Soft-Warn (Correct) |
|---|---|---|
| Schema validation fails | Return verdict=FAIL immediately | Log warning, continue to verifier |
| Artifacts missing | Override PASS to NEEDS_HUMAN | Log gap, trust verifier judgment |
| Liveliness check | Downgrade FAIL to NEEDS_HUMAN if verifier ran <60s | Log brief activity as note, trust verdict |
| Contract path missing | Hard error, abort flow | Fall back to LLM contract generation |

## Related Patterns

- [[Verify-Fail-Retry Loop]] — cycles verifier feedback back to coder for self-correction
- [[Agent Stall Recovery]] — restarts stuck agents rather than failing the whole workflow

## Sources

- BD-pairv2-schema-hard-fail: schema validation hard-fail removed
- BD-pairv2-artifacts-hard-fail: required-artifacts gate removed
- BD-pairv2-liveliness-override: liveliness timing override removed
- BD-pairv2-llm-driven-failsoft-files: missing files fall back to LLM generation
- BD-pairv2-flatten-session-dir: process exit as primary completion signal
