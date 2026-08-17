---
title: "Campaign summary prompt — multi-model design review of a chronological campaign summarization prompt"
type: source
tags: [prompt-engineering, campaign-summary, summarization, chronological-summary, multi-model-review, chatgpt, gemini, cursor, dm-assistant, transcript-processing]
sources: [2026-08-04-campaign-summary-prompt-design]
last_updated: 2026-08-04
---

# Campaign Summary Prompt — Multi-Model Design Review

**Source**: Working document "campaign summary prompt" — a draft LLM prompt for generating strict chronological summaries of role-playing campaign transcripts, plus design feedback collected from three model surfaces: [[ChatGPT]], [[Gemini]] via [[GoogleAIStudio]], and Gemini via [[Cursor]]. This is a meta-document (prompt engineering for the campaign pipeline), not a campaign bible — it defines the [[CampaignSummaryPrompt]] used to compress long campaign transcripts into canonical event timelines.

## The Prompt Itself

**Role**: AI as meticulous Game Master's assistant. **Objective**: given a complete raw campaign transcript (player inputs, GM outputs, narrative, game state updates), produce a **strict chronological bullet-point summary** of all major, canonical events and significant state changes.

**Content requirements per bullet**:
- Strict chronological order matching the campaign sequence
- Key events and plot points: narrative developments, mission completions, discoveries, pivotal twists
- PC actions and progress: major decisions and outcomes, level-ups ("PC reaches Level X: brief summary of major gains"), major power-ups/ability acquisitions/transformations (e.g. "PC gains Senju cells", "PC awakens Rinnegan"), significant resource gains/losses
- Key NPC status changes (document truncates mid-section here)

## Multi-Model Feedback

### ChatGPT
1. **Chronology handling**: transcripts may lack timestamps — should the AI infer sequence solely from transcript order, or will date markers be supplied? Add instructions for ambiguous timing.
2. **Bullet granularity**: "significant" is underspecified — suggest a minimum-impact guideline (XP awards, mission completions) to avoid overly granular bullets. See [[SignificanceThreshold]].
3. **Retcon tracking**: specify formatting for multiple retcons per session, e.g. "DM Note Retcon (Session 3): ...". See [[RetconDMNote]].
4. **Transcript length and chunking**: very long campaigns need segmented processing — instruct on partial transcripts and iterative summarization. See [[TranscriptChunkingSummarization]].
5. **Output metadata**: optional timestamp or sequence identifier per bullet for later referencing.

### AI Studio Gemini
1. **Definition of "significant"**: optionally add "Significance is determined by narrative impact, changes to core character power/status, or advancement of primary plotlines" — though examples probably suffice.
2. **Conciseness vs detail for power-ups**: the model must pick truly major gains. Worked example: [[ItachiUchiha]]'s monumental Level 20 compresses to "Gains Perfect Susano'o, Totsuka Blade, Yata Mirror, Senju Life Force Mastery, and refined ocular/chakra control."
3. **Player choice handling**: think blocks are excluded from summaries, but the AI should capture the *resolution* of a think block (the CHOICE_ID selected) and summarize the decision plus immediate outcome. See [[ThinkBlockChoiceResolution]].

### Cursor Gemini
Verdict: "ready to go as-is", with optional polish:
1. **Inferring significance fallback**: "If an event's significance is ambiguous, err on the side of including it" — capture all potentially pivotal moments.
2. **Off-screen events**: summarize events at the point of *revelation* in the narrative, not at their chronological occurrence — e.g. a betrayal revealed months later becomes "Character X reveals they betrayed the party" placed at the reveal. See [[OffScreenEventRevelation]].

## Significance for the Wiki Pipeline

This prompt is upstream of campaign ingestion: it defines how raw transcripts (like the [[NocturneSosuke]] and [[NocturneRavencrest]] campaign lines) get compressed into canonical event summaries. The three reviews converge on the same gaps — significance is fuzzy, chronology-vs-revelation ordering needs a rule, and long transcripts need chunking — which are exactly the failure modes seen in transcript-order ingestion. Notably, all three models independently accepted the core structure; disagreement was confined to edge-case handling.