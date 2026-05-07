---
title: "Skeptic Gate 8"
type: concept
tags: [skeptic, gate, alignment, llm-evaluation]
date: 2026-04-24
---

## Definition

Skeptic Gate 8 is the alignment gate requiring "PR description goals, scope, tenets, diff, and evidence must agree." It is defined at `skeptic/prompt.ts:174`. It uses the `skeptic-gate-8` marker at `prompt.ts:211`.

## Scope

Gate 8 is the high-level alignment requirement. It is enforced by:
- Rule 11 (design alignment) — explicit deterministic checks 11a-11f
- Rule 12 (goals verification) — deterministic ## Goals parser

**Known gap**: Gate 8 covers "tenets" and "scope" in its wording but there is NO dedicated deterministic parser for tenets/scope equivalent to Rule 12's Goals parser. A tenets-only PR would pass Rule 12 (skip, since no Goals section) even if tenets were absent from the diff.

## See Also

- [[skeptic-gate-7]] — Technical review gate
- [[skeptic-rule-12]] — Goals verification rule
- [[tenets-gap]] — The tenets/scope parser gap
- [[skeptic-agent]]
