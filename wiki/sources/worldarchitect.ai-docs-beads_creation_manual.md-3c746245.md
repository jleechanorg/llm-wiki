---
title: "Manual Beads Creation Guide"
type: source
tags: [worldarchitect-ai, evaluation-feedback, game-state, bugs, fixes]
sources: []
date: 2026-01-12
source_file: raw/manual-beads-creation.md
last_updated: 2026-04-07
---

## Summary
Evaluation feedback analysis identifying 13 critical game state issues in WorldArchitect.AI D&D 5e gameplay including context hallucination where AI responds about wrong entities, monotonic counter violations (XP decreasing), and missing transparency in game calculations (FP, gold, capacity).

## Key Claims
- **Critical: Context Hallucination** — Player asks to attack "Golden Dawn" but AI responds about "Blood Ravens" from previous scene
- **Critical: Monotonic Counter Violation** — XP decreased from 800/900 to 550/900 across scenes 16-17
- **Major: FP Calculation Opaque** — FP jumped from 5,750 to 12,000 with no player action
- **Major: Gold Ledger Missing** — Gold jumped from 331 to 26,756 (+26,425) in one week with no breakdown
- **Major: Unit Category Contradiction** — Narrative says "5,000 total personnel" but status shows 4,281 soldiers
- **Major: HP/HD Not Tracked** — Level 5 Fighter still has 20/20 HP and HD 1/1 (should be 5 total)

## Key Quotes
> "XP decreased from 800/900 to 550/900 in Scene 16-17. Add server-side validation enforcing monotonic counters for XP, gold, territory." — Priority 1 bug

> "FP jumped from 5,750 to 12,000 with no action. Show FP components and delta breakdown in prompts." — Priority 2 feature

> "Gold jumped from 331 to 26,756 (+26,425) in one week. Add weekly/turn ledger block showing income sources and expenses." — Priority 2 feature

## Connections
- [[WorldArchitectAI]] — main platform these bugs were found in
- [[DungeonsAndDragons]] — game system being played
- [[Beads]] — distributed git-backed issue tracker where these issues should be filed

## Contradictions
- None detected with existing wiki content — this is new evaluation feedback

## Priority 3 Issues
- **Capacity Formula** — Max citizens jumps without explanation (25,000/26,150 → 25,425/33,100)
- **XP Pacing** — Jumped from Level 2 to Level 5 in single combat (9,400 XP)
- **Economic Rebalancing** — Economy scales from tight (24gp) to trivial (26,756gp) in one week
- **Ranking Stagnation** — Rank stays #100/201 despite major victories
- **Inconsistent Costs** — Farms 500gp/5, fortifications "at least 100gp"