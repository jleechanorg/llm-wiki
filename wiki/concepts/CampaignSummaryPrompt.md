---
title: "Campaign Summary Prompt"
type: concept
tags: [prompt-engineering, summarization, campaign-pipeline, chronological-summary, dm-assistant]
sources: [2026-08-04-campaign-summary-prompt-design]
last_updated: 2026-08-04
---

# Campaign Summary Prompt

A prompt template that turns a complete raw RPG campaign transcript (player inputs, GM outputs, narrative, game state updates) into a **strict chronological bullet-point summary** of major, canonical events and significant state changes. The AI's role is a "meticulous Game Master's assistant."

## Required content per bullet
- Key events and plot points (missions, discoveries, twists)
- PC decisions and their direct outcomes
- Level-ups with a brief summary of major gains (see the [[ItachiUchiha]] Level 20 example)
- Major power-ups, ability acquisitions, transformations
- Significant resource gains/losses; key NPC status changes

## Open design questions (from the 2026-08-04 tri-model review)
- [[SignificanceThreshold]] — what counts as "significant", and the err-toward-inclusion fallback
- [[RetconDMNote]] — formatting multiple retcons in one session
- [[TranscriptChunkingSummarization]] — segmented/iterative processing of very long campaigns
- [[OffScreenEventRevelation]] — place events at revelation, not chronological occurrence
- [[ThinkBlockChoiceResolution]] — exclude think blocks but capture the chosen CHOICE_ID's resolution

Reviewers: [[ChatGPT]], [[Gemini]] via [[GoogleAIStudio]], and Gemini via [[Cursor]]. All accepted the core structure; feedback was confined to edge cases.