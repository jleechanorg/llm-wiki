---
title: "Clean-Slate Campaign Restart"
type: concept
tags: [campaign-management, llm-dm, context-migration, prompt-pattern]
sources: [2026-08-04-aizen-mortal-campaign-shadow-over-the-gate-start]
last_updated: 2026-08-04
---

# Clean-Slate Campaign Restart

Player prompt pattern for LLM-DM campaigns: "Look at [prior chat] for context but start a new campaign... Same characters and factions but start with a clean state."

The pattern separates **world assets** (cast, factions, setting) from **campaign state** (levels, positions, consequences): the LLM is told to carry the former across chats while zeroing the latter. Used to spawn [[ShadowOverTheGate]] from the "bane - main" chat, preserving [[AizenSosuke]], the Bane thread ([[CultOfTheDeadThree]]), and the [[BaldursGate]] faction web.

Contrast with [[CampaignContextMigration]] (chat 2 of the god campaign), which does the opposite: carries FULL state — prior chat log, campaign info, reference files — into a fresh chat purely to escape a context-length limit. Together they form the two poles of LLM campaign continuity: restart-with-assets vs migrate-with-state.