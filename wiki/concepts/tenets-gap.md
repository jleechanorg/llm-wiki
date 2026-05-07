---
title: "Tenets Gap in Skeptic Gate 8"
type: concept
tags: [skeptic, gap, tenets, scope, gate-8]
date: 2026-04-24
---

## Definition

The "Tenets Gap" is the observation that Gate 8 in the skeptic prompt covers "tenets" and "scope" in its alignment requirement, but there is NO dedicated deterministic parser for tenets or scope equivalent to Rule 12's Goals parser.

## The Problem

Gate 8 states: "PR description goals, scope, tenets, diff, and evidence must agree."

But only `## Goals` / `## Goal` sections have a deterministic extraction and diff-evidence check (Rule 12). If a PR author writes:

```
## Tenets
- All API responses must be typed
- No use of `Any` for structured data
```

...and the diff contains `result: dict[str, Any]` with no TypedDict, the tenets check has no deterministic enforcement. It would be left to the LLM's judgment in Gate 8, which is non-deterministic and unreliable.

## Implication

A PR could have completely unmet tenets and pass the skeptic review if:
1. It has no ## Goals section (skip Rule 12)
2. It has a ## Tenets section with unmet tenets
3. The LLM in Gate 8 doesn't catch the gap (LRM unreliability)

## The Fix

Add Rule 12-equivalent for tenets/scope:
- Extract `## Tenets` and `## Scope` sections from PR description
- Parse bullet items
- Check each tenet/scope bullet against diff evidence
- FAIL if any tenet/scope has no corresponding diff evidence

## See Also

- [[skeptic-gate-8]] — The alignment gate containing tenets/scope
- [[skeptic-rule-12]] — The Goals parser (the model for the fix)
- [[skeptic-agent]] — Parent agent
