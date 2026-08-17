---
title: "Aizen god campaign — mortal-era chat opening: ChatGPT-to-Gemini DM handoff via master prompt"
type: source
tags: [campaign, dnd-5e, aizen, dm-handoff, prompt-engineering, meta, gemini, chatgpt]
sources: [2026-08-04-aizen-god-campaign-chat-mortal]
last_updated: 2026-08-04
---

# Aizen God Campaign — Mortal-Era Chat: The DM Handoff

**Source**: Opening of the "mortal" chat in the Aizen god-campaign lineage. Unlike the sibling chats ([[2026-08-04-aizen-god-campaign-chat-1|chat 1]], [[2026-08-04-aizen-god-campaign-chat-2|chat 2]]), this segment contains **no in-fiction campaign content**. It is the meta-conversation in which the player asks [[Gemini]] how to migrate an ongoing D&D-style campaign from [[ChatGPT]] to Gemini, and Gemini responds with a complete migration methodology.

## What this is

The player was running a D&D-style campaign on ChatGPT and asked Gemini: *"if i wanna switch the context to you how would i do it."* Gemini frames the problem as "bringing a new Dungeon Master up to speed mid-campaign" and prescribes the [[MasterPromptCampaignHandoff]] technique — a single comprehensive context-transfer prompt rather than pasting raw chat logs.

## The handoff methodology (as prescribed by Gemini)

**Step 1 — Gather core campaign information** (summary beats transcript):
1. High-level campaign summary — one-paragraph elevator pitch: main conflict + tone (heroic fantasy, grimdark, political intrigue)
2. PC sheets — name/race/class/level, key stats, personality, motivation, backstory hooks
3. "Previously On..." recap — current physical location, last action taken; this is the resume point
4. World state — major NPCs (with relationship: ally/foe/quest-giver), factions, key locations
5. Active quests and unresolved plot hooks
6. Important inventory — unique magic items, plot objects, consumables remaining

**Step 2 — Craft the master prompt** using a fill-in template. Gemini supplies a worked example populated with illustrative placeholder content (campaign "The Whispering Shadow"; example PCs Kaelen the High-Elf Wizard, Bror the Dwarf Barbarian, Seraphina the Human Rogue; quest-giver Elara; antagonist Cult of the Whispering Shadow led by "The Veil"; the Sunken Temple of Sezath). **These are template examples, not actual Aizen-campaign entities** — the real campaign roster ([[AizenSosuke]], [[BaldursGate]] factions, etc.) appears in the sibling chats.

**Key structural elements of the template**: numbered sections (Campaign Overview → PCs → Current Situation → NPCs & Factions → Active Quests → Inventory), an explicit role assignment ("be a descriptive, fair, and creative DM"), and a resume directive (acknowledge context, then narrate the results of the party's in-progress actions).

## Significance for the campaign lineage

This handoff explains how the Aizen campaign's rich state — later visible in [[2026-08-04-aizen-campaign-summarized|the summarized arc]] — could survive a platform migration. It is the practical companion to [[CleanSlateCampaignRestart]]: where clean-slate restarts reuse characters but reset state, the master-prompt handoff preserves full state across a change of DM substrate. It is also the origin point of the [[CampaignContextMigration]] pattern later executed between Gemini chats 1 and 2.

## Key design insights

- **Summary over transcript**: Gemini explicitly advises against pasting the entire chat log — a curated state snapshot transfers better than raw history.
- **State, not story**: the template captures resumable *state* (location, resources, open quests, NPC dispositions), not narrative prose.
- **Explicit role + resume point**: the prompt ends with a concrete "start here" action so the new DM produces continuation, not recap.
