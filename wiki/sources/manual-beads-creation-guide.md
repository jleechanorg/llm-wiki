---
title: "Manual Beads Creation Guide"
type: source
tags: [beads, evaluation-feedback, game-state, bugs, prompt-engineering]
source_file: "raw/manual-beads-creation-guide.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Operational guide for manually creating beads (issue tracking entries) based on evaluation feedback analysis. Documents 13 priority issues (Priority 1-3) covering game state consistency, prompt engineering, character progression, and economic balancing for what appears to be a D&D-style game system.

## Key Claims

### Priority 1 (Critical)
- **Context Hallucination**: Player asks to attack "Golden Dawn" but AI responds about "Blood Ravens" from previous scene — requires intent/entity matching guardrail
- **Monotonic Counter Validation**: XP decreased from 800/900 to 550/900 — needs server-side validation enforcing monotonic counters

### Priority 2 (Major)
- **FP Calculation Transparency**: FP jumped from 5,750 to 12,000 with no action — requires breakdown display
- **Gold Ledger Block**: Gold jumped from 331 to 26,756 (+26,425) in one week — needs ledger tracking
- **Unit Category Clarification**: Troop counts contradict (5,000 vs 4,281) — needs canonical representation
- **Turn Advancement Mechanics**: All scenes in Turn 1 despite major campaign — needs strategic tick definition
- **HP and Hit Dice Tracking**: Level 5 Fighter has 20/20 HP instead of proper scaling — needs level-up tracking

### Priority 3 (Medium)
- **Capacity Formula**: Max citizens jumps unexplained — needs breakdown display
- **XP Pacing Caps**: Level 2→5 jump in single combat — needs encounter caps
- **Economic Income Rebalance**: Economy scales too fast — needs upkeep costs
- **Ranking Calculation**: Rank stays #100 despite victories — needs recalibration
- **Fail-Forward Mechanics**: Failed rolls inconsistent — needs standardization
- **Construction Costs**: Inconsistent costs — needs standardization

## Usage
These beads can be created manually using the MCP beads tool or tracked in the analysis document until the MCP tool JSON parsing issue is resolved.
