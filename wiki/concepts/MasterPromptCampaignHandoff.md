---
title: "Master Prompt Campaign Handoff"
type: concept
tags: [prompt-engineering, dm-handoff, context-migration, dnd-5e, state-transfer]
sources: [2026-08-04-aizen-god-campaign-chat-mortal]
last_updated: 2026-08-04
---

# Master Prompt Campaign Handoff

A context-migration technique for moving an ongoing LLM-DM'd campaign to a new DM substrate using **one comprehensive state-transfer prompt** instead of pasting raw chat logs. Prescribed by [[Gemini]] in the [[2026-08-04-aizen-god-campaign-chat-mortal|Aizen mortal-era chat]] when the player asked how to migrate a campaign from [[ChatGPT]].

## The method

**Step 1 — Gather core campaign information** (summary beats transcript):
1. High-level campaign summary — elevator pitch: main conflict + tone
2. PC sheets — name/race/class/level, key stats, personality, motivation, backstory hooks
3. "Previously On..." recap — current location + last action taken (the resume point)
4. World state — major NPCs with relationship tags (ally/foe/quest-giver), factions, key locations
5. Active quests and unresolved plot hooks
6. Important inventory — unique magic items, plot objects, consumables

**Step 2 — Craft the master prompt** from a fill-in template with numbered sections (Campaign Overview → PCs → Current Situation → NPCs & Factions → Active Quests → Inventory), an explicit role assignment ("be a descriptive, fair, and creative DM"), and a resume directive (acknowledge context, then narrate results of in-progress actions).

## Design principles

- **Summary over transcript** — a curated state snapshot transfers better than raw history.
- **State, not story** — capture resumable state (location, resources, open quests, NPC dispositions), not narrative prose.
- **Explicit role + resume point** — end the prompt with a concrete "start here" action so the new DM produces continuation, not recap.

## Relationship to sibling patterns

- [[CampaignContextMigration]] — the *executed* migration between Gemini chats 1 and 2 (which, notably, DID include the full prior chat log alongside campaign info and prompts — a heavier variant than this technique prescribes).
- [[CleanSlateCampaignRestart]] — the contrasting pattern: characters reused, state deliberately reset.
- [[LLMDMPlatformMigration]] — the general cross-platform migration problem this technique solves.

## Template placeholder caveat

Gemini's worked example (campaign "The Whispering Shadow"; PCs Kaelen, Bror, Seraphina; antagonist "The Veil"; the Sunken Temple of Sezath) is **illustrative placeholder content only** — none of these are real Aizen-campaign entities.
