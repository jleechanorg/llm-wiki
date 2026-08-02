---
title: "High-Tier Personal-Scale Challenge"
type: concept
tags: [campaign-design, worldarchitect, prompt-engineering, escalation-prevention, npc-density]
date: 2026-07-27
sources:
  - /Users/jleechan/.hermes/visenya_v9_diagnosis_2026-07-26/diagnosis.md
  - /Users/jleechan/.hermes/visenya_v9_diagnosis_2026-07-26/summary.md
  - /Users/jleechan/llm_wiki/wiki/sources/qoqthsu7dxznr24vnu9w-qoQtHsU7.md
inspired_by_campaign: visenya-v9
---

# High-Tier Personal-Scale Challenge

## Definition

In an escalating CRPG/TRPG-style LLM-driven campaign, **personal-scale challenge** is the dramatic register where player and NPC stand close enough in narrative power that *a single choice* (a disguise, a lie, a withheld word, a deferred payment) can resolve or doom the immediate situation. High-tier personal-scale challenge is the deliberate **preservation of that register** even when the player character has scaled past the parity band — i.e., the PC is now level 20 but the LLM continues to offer scenes at the level-6-to-10 dramatic register (disguise games, peer-tier betrayals, household politics) rather than auto-escalating to mythic-tier antagonists.

## Why it matters

Discovered 2026-07-27 from the Visenya v9 campaign analysis (campaign_id `qoQtHsU7DxZnR24VNU9w`, 412 scenes spanning levels 6-21, 47 named NPCs). Player feedback: "Campaign felt more dynamic and challenging under level 15; I liked zero-sum consequences I can't please anyone but the LLM should hide consequences from me until later."

Quantitative finding: pre-level-15 scenes had **23.6% two-way dialog** vs **18.0%** post-level-15; the loss of two-way exchanges correlated with scenes collapsing to 1-2 named NPCs of mythic tier, vs 3-4 distinct peer NPCs in pre-level-15 scenes.

## Relationship to other concepts

- **Escalation Creep** — opposite problem; mythic-tier by default is a failure of this principle.
- **NPC Density** — a high-tier personal-scale scene still has 3-5 named NPCs each with private agendas.
- **Consequence-Hiding** — the user's preferred dramatic register *requires* asymmetric disclosure of consequence.
- **Social HP / Victory Ripple** — mechanics exist in `narrative_system_instruction.md` but their effect vanishes at high tier without explicit preservation rules.

## Prompt-only implementation

Five edits to `mvp_site/prompts/*.md` files (no backend enforcement):

1. **Tier Compression** (new section in `narrative_system_instruction.md`) — preserve parity-band named NPCs across levels.
2. **Consequence-Hiding Heuristic** (rewrite NPC Autonomy section in `narrative_system_instruction.md`) — make asymmetric disclosure a heuristic rule.
3. **High-tier NPCs are still people** (add row to `dialog_system_instruction.md` §1.1) — prevent monolithic-elder NPC conflation.
4. **Force-a-trade** (rewrite `dialog_system_instruction.md` §5.3) — replace flat refusals with named-cost offers.
5. **Anti-creep on major events** (edit `living_world_instruction.md` Major Event Rarity Budget) — prefer personal-scale to mythic-scale when both possible.

Full text of the five edits at `/Users/jleechan/.hermes/visenya_v9_diagnosis_2026-07-26/diagnosis.md`.

## Verification recipe

Run a campaign through a high-tier arc with these prompts in place. Compare per-scene JSONL of pre-fix vs post-fix using the analyzer at `/tmp/analyze_visenya_v9_v2.py`. Expect:
- Two-way dialog % in high-tier scenes rebounds from 18 → 22+
- Number of distinct named NPCs per scene stays ≥3 through level 20+
- NPC body-language / frequency distinctness maintained

## Related sessions
- 2026-07-26: Visenya v9 ingest + diagnosis.

## Cross-references
- [[Visenya-v9-campaign]]
- [[Campaign-PromptArchitecture]]
- [[Living-World-Infrastructure]]
