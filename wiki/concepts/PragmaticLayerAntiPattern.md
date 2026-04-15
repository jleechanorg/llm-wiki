---
title: "Pragmatic Layer Anti-Pattern"
type: concept
tags: [anti-pattern, design-drift, architecture, PR-practice]
date: 2026-04-15
---

## Definition

"Pragmatic Layer N" is an anti-pattern where a PR claims to implement a design phase/layer but explicitly admits it does not meet the stated design gates. The admission is buried in the PR body rather than being fixed before merge.

## Example

From PR #6276 body:

> "This PR achieves **pragmatic Layer 3 CLEAN**: world_logic delegates to rewards_engine via project_level_up_ui() with no duplicate XP math and the single-call invariant honored. The aspirational v4 design (world_logic as 'thin modal wrapper only') was not fully achieved — orchestration wrappers remain at lines 1246, 1669, 1695, 1715."

Translation: "The design says ZERO public API calls. We have 21. But we're calling it done anyway."

## Why This Is An Anti-Pattern

1. **Gates are not optional**: The design doc exit gates exist to prevent accumulated debt. Claiming "pragmatic" bypasses the check.
2. **Merge confusion**: Reviewers cannot tell if the PR meets the design or not.
3. **Future work untracked**: The gaps are acknowledged but not tracked as follow-up work.
4. **Verifiability lost**: If gates can be declared "good enough" informally, any design doc becomes optional.

## Correct Response

When a design gate cannot be met:

| Option | When to Use | Action |
|--------|------------|--------|
| **Update the design doc** | Gate was wrong or superseded | Revise gate to achievable state, document why |
| **Track as follow-up** | Gate valid but blocked | Create bead, commit to timeline |
| **Decline the PR** | Gate valid and achievable | Do not merge until gate passes |
| **Negotiate scope** | Gate valid but too expensive | Renegotiate milestone, don't fake it |

## Key Rule

> **"Pragmatic" does not mean "skip verification." If a gate cannot pass, the gate must be explicitly updated (with reason) before the PR is merged. The verifier will catch you.**

## Connections

- [[DesignDocGateVerification]] — the correct pattern: verify gates independently
- [[DesignDocAsContract]] — treat design docs as checkable, not optional
- [[StructureDriftPattern]] — pattern of design doc vs code divergence over time
- [[PRWatchdog]] — monitor for pragmatic-layer admissions in PR bodies

## Related Anti-Pattern

The "Architecture Note" pattern — where a PR documents its own architectural debt in a section that is essentially a disclaimer: "Yes we know this is broken, but we're merging anyway." This is distinct from "known limitations" which are appropriately scoped. An Architecture Note implies the design was not met, without a plan to fix it.