---
title: "Campaign Context Migration (LLM chat handoff)"
type: concept
tags: [llm-dm, workflow, context-window, gemini, campaign-continuity]
sources: [2026-08-04-aizen-god-campaign-chat-2]
last_updated: 2026-08-04
---

# Campaign Context Migration

The player's practiced workflow for continuing a long-running LLM-DM'd campaign across chat-session boundaries, demonstrated at the top of [[2026-08-04-aizen-god-campaign-chat-2]] when chat 1 hit its length limit.

## The protocol

The player opens a fresh chat and supplies four artifacts, with the stated goal that the seam be invisible ("so I don't even realize I made a new chat"):

1. **Overall campaign information** — world summary, plot, key NPCs, house rules.
2. **Full chat log** of the previous session(s).
3. **Reference files** — with explicit usage constraints (ASOIAF books marked *style-only*: no characters or places may be imported), plus an instruction that the DM flag any conflicts.
4. **Original prompts/instructions** — the campaign's system-prompt layer, re-sent verbatim.

The DM (Gemini) confirms the intake contract before receiving a **definitive campaign export** — a player-authored save file enumerating premise, character build, every resource pool, and all active abilities.

## Why it matters

- This is player-side **state serialization for stateless LLMs**: the export doubles as an authoritative canon document, resolving any drift the raw chat log might contain. Related in-campaign concepts: [[CleanSlateCampaignRestart]] (reset variant, chat 1) vs. this **seamless-continue** variant — same artifact set, opposite intent for state.
- The "flag conflicts in reference files" clause delegates consistency-checking to the DM — an early, informal version of ingestion contradiction-detection.
- Structurally identical to the compaction-handoff problem in agent harnesses: continuity depends on what the author chose to serialize, and the export's numbers (not the prior transcript) become ground truth going forward.

## Links

- [[CleanSlateCampaignRestart]] — the reset-flavored sibling protocol
- [[Whispers-of-the-Realm]] — DM-side narrative state tracking in the sibling campaign
- Source: [[2026-08-04-aizen-god-campaign-chat-2]]
