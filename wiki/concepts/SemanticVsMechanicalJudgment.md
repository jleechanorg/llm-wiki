---
title: "Semantic Vs Mechanical Judgment"
type: concept
tags: [zfc, ai-judgment, architecture, classification]
sources: [ZeroFrameworkCognition]
last_updated: 2026-04-11
---

# Semantic vs Mechanical Judgment

The central distinction in Zero Framework Cognition (ZFC): **semantic judgment** must be delegated to AI, while **mechanical judgment** belongs in application code.

## The dividing line

| Semantic (delegate to AI) | Mechanical (code handles) |
|---------------------------|---------------------------|
| What does this text mean? | Does this text parse as valid JSON? |
| Which intent does this match? | Does this string contain a keyword? |
| What is this image? | Is this pixel data a PNG header? |
| How important is this item? | Is this number within range? |
| Which story moments matter? | Does this string match a regex pattern? |

## Why the distinction matters

Application code that makes semantic judgments:
1. **Brittle**: keyword lists and heuristics miss edge cases
2. **Wrong**: hardcoded rankings reflect developer assumptions, not reality
3. **Obsolete**: patterns that worked at training time drift over time

## Examples from worldarchitect.ai

**Mechanical (ZFC-compliant):**
- `level_from_xp()` — D&D 5e threshold lookup (mechanical rule)
- `validate_game_state_updates()` — XP/level clamping, time monotonicity
- `dice_rolls` regex parsing — language-agnostic pattern matching

**Semantic (violates ZFC):**
- `intent_classifier.py` — FastEmbed cosine similarity against anchor phrases (semantic routing via local model)
- `_get_backpack_importance()` — keyword tier scoring for item importance
- `MIDDLE_COMPACTION_KEYWORDS` — 50+ keywords filter story context

## The FastEmbed exception

FastEmbed in `intent_classifier.py` uses a local embedding model (~133MB) for latency reasons. This is a **gray area**: it's local AI, but it's still making semantic classification decisions via heuristic similarity scoring, not via an LLM that can reason about intent.

User guidance: FastEmbed is acceptable for latency if the anchor phrases are regularly updated and the similarity threshold is tuned. The risk is drift — anchor phrases trained today may not match user inputs next month.

## Related
- [[ZeroFrameworkCognition]] — full ZFC framework
- [[StructureDriftPattern]] — fields accidentally nested inside wrong conditional blocks (a type of mechanical judgment leakage)
