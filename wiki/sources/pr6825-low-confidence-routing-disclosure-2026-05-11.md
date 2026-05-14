---
title: "PR 6825 Low-Confidence Routing Disclosure"
type: source
tags: [worldarchitect, routing, zfc, pr-6825]
date: 2026-05-11
source_file: raw/pr6825-low-confidence-routing-disclosure-2026-05-11.md
sources: []
last_updated: 2026-05-11
---

## Summary

PR #6825 should not absorb faction-routing hardening unless that routing issue directly blocks the 20-turn core-memory proof. The routing fix belongs in a separate follow-up by default and should use disclosure-first classifier metadata instead of heuristic context suppression.

## Key Claims

- A Kira/Alexiel NPC-addressed prompt routed to `FactionManagementAgent` at weak classifier confidence (`0.663`), showing a low-margin ambiguity problem.
- The correct near-term PR #6825 path is to keep memory evidence scoped: same-head smoke cleanup, exactly 20 natural proof turns, real traces, and artifact-true PR text.
- Faction routing should be fixed later unless the 20-turn proof cannot pass without it.
- The safer routing hardening is to expose top-N scores, margin, and context influence to the selected agent LLM so it can preserve NPC/dialog framing.
- Context capping or suppression should be a last resort because it can drift into heuristic routing.

## Connections

- [[LowConfidenceRoutingDisclosure]] — captures the disclosure-first routing pattern.
- [[AgentRouting]] — the broader WorldArchitect agent-selection surface.
- [[ZeroFrameworkCognition]] — forbids keyword/regex heuristic intent routing.
- [[WorldArchitectAI]] — project context.

## Contradictions

- None known. This refines earlier "cap/ignore context" language by making disclosure-first the preferred path.
