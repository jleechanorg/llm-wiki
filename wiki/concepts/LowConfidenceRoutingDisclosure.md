---
title: "Low Confidence Routing Disclosure"
type: concept
tags: [agent-routing, zfc, intent-classification, worldarchitect]
sources: [pr6825-low-confidence-routing-disclosure-2026-05-11]
last_updated: 2026-05-11
---

## Summary

Low Confidence Routing Disclosure is a ZFC-compatible pattern for weak semantic classifier matches: keep the classifier decision visible, but disclose its uncertainty to the selected agent LLM rather than adding keyword heuristics or silently suppressing context.

## Pattern

When a specialized route wins by a weak score or narrow margin:

- Record selected mode, selected score, top-N candidates, runner-up margin, and whether prior context influenced the score.
- Pass a compact uncertainty note into the selected agent prompt/debug metadata.
- Let the selected agent LLM preserve the user's framing when the route is ambiguous, especially for NPC-addressed dialogue.
- Add regression coverage for weak specialized-route cases and strong specialized-route cases.

## Anti-Pattern

Do not replace this with:

- keyword checks such as "if the text says Kira, force dialog",
- regex intent overrides,
- hardcoded phrase-to-agent routing,
- unproven context suppression rules.

Context capping or ignoring can be considered only after evidence shows disclosure is insufficient, and then it should be documented as classifier calibration rather than semantic keyword routing.

## PR 6825 Application

For PR #6825, faction routing should remain a separate follow-up unless the 20-turn core-memory proof cannot pass without it. The PR's primary closeout remains current-head 20-turn core-memory evidence plus real smoke cleanup.

## Related

- [[AgentRouting]]
- [[AgentSelection]]
- [[ZeroFrameworkCognition]]
- [[WorldArchitectAI]]
