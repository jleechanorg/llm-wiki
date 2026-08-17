---
title: "DM Bookkeeping Trust Gap"
type: concept
tags: [dm-behavior, llm-dm, bookkeeping, audit, campaign-pattern]
sources: [2026-08-04-aizen-god-campaign-chat-1-301-600]
last_updated: 2026-08-04
---

# DM Bookkeeping Trust Gap

Pattern where an (LLM) DM **asserts** a derived character-sheet value without showing the calculation, leaving the player unable to verify correctness — and where the player compensates by routinely auditing DM math.

## Canonical instance

In [[2026-08-04-aizen-god-campaign-chat-1-301-600|Aizen god campaign chat 1 (301-600)]], the Level 9→10 advancement (Bard 7→8) did not visibly recalculate HP; the DM asserted 59 HP "already reflected Bard 8" with no shown derivation. A level gained should normally add a hit-die worth of HP, so an unchanged total asserted-without-math is exactly the kind of claim that needs an audit.

## Why it matters for LLM DMs

- LLM DMs confabulate plausible-sounding sheet states; unshown derivations are unfalsifiable at the table.
- Homebrew layers ([[DestinyRulebookOverrides]], stacked attribute bonuses from [[Bane]] heritage + legendary items + ASIs) multiply the arithmetic surface and thus the confabulation risk.
- The observed mitigation is player-side: audit every derived number and demand recomputation — the DM's "thank you for holding me to account" framing shows the audit loop working socially but not structurally.
- Structural mitigation would be showing work by default (analogous to [[NarratorBugCorrection]] in sibling campaigns): every level-up posts the full before/after derivation.

Related: [[PlayerDirectedExpGrant]], [[Whispers-of-the-Realm]].
