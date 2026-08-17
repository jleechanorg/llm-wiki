---
title: "LLM DM Platform Migration"
type: concept
tags: [context-migration, dm-handoff, llm-platforms, campaign-continuity]
sources: [2026-08-04-aizen-god-campaign-chat-mortal, 2026-08-04-aizen-god-campaign-chat-2]
last_updated: 2026-08-04
---

# LLM DM Platform Migration

The general problem of moving an ongoing LLM-DM'd campaign **across DM substrates** — either between products ([[ChatGPT]] → [[Gemini]]) or between chats on the same product (Gemini chat 1 → chat 2 at the length limit) — while preserving campaign continuity.

## Observed instances in the Aizen lineage

1. **Cross-platform (ChatGPT → Gemini)**: solved via the [[MasterPromptCampaignHandoff]] — a single curated state-snapshot prompt with role assignment and resume directive ([[2026-08-04-aizen-god-campaign-chat-mortal|mortal-era chat]]).
2. **Intra-platform (Gemini chat 1 → chat 2)**: solved via [[CampaignContextMigration]] — a heavier bundle of (a) overall campaign information, (b) the full prior chat log, (c) style-only reference files, and (d) the original campaign prompts.

## Key insight

The two instances weigh the transcript differently: the cross-platform handoff explicitly advises *against* pasting raw logs (summary over transcript), while the intra-platform continuation *includes* the full prior log. The difference tracks context-window economics — a fresh chat on the same platform can afford (and benefits from) the full log; a cross-platform prompt must be compact and self-contained.

## Related

- [[MasterPromptCampaignHandoff]] — the compact cross-platform technique
- [[CampaignContextMigration]] — the full-log intra-platform variant
- [[CleanSlateCampaignRestart]] — the deliberate non-migration alternative (reset state, keep characters)
