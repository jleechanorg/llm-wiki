---
title: "Skeptic Rule 12"
type: concept
tags: [skeptic, rule, goals, deterministic, llm-evaluation]
date: 2026-04-24
---

## Definition

Rule 12 is the deterministic Goals-section verification rule in the skeptic prompt. It extracts bullet/numbered items from a `## Goals` or `## Goal` section in the PR description and verifies each has diff evidence. Defined at `skeptic/prompt.ts:159-168`.

## Rule 12 Logic

1. If PR has no Goals section — skip (not mandatory)
2. Extract each bullet/numbered item from Goals section
3. For each goal, verify there is diff evidence (code, config, workflow, or other changes)
4. **FAIL** if any goal has NO corresponding implementation in the diff
5. Feature/bugfix goals with only test changes = NOT implemented (tests prove behavior, not create it)
6. Goals explicitly about tests = CAN be satisfied by test changes only
7. Documentation-only goals = require only doc changes

## Key Insight

Rule 12 is the STRONGEST enforcement in the skeptic prompt because it is deterministic and explicit. It works even without LLM reasoning — the LLM is just interpreting and matching. By contrast, Gate 8's "tenets" and "scope" checks rely entirely on LLM interpretation without a dedicated deterministic parser.

## See Also

- [[skeptic-gate-7]] — Technical review gate
- [[skeptic-gate-8]] — Alignment gate (Rule 12 is part of Gate 8 enforcement)
- [[tenets-gap]] — The gap for tenets/scope (no equivalent to Rule 12)
- [[skeptic-agent]]
