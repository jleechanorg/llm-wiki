---
title: "Think-Block Choice Resolution (summarize the decision, not the deliberation)"
type: concept
tags: [summarization, player-choice, think-blocks, choice-id, prompt-engineering]
sources: [2026-08-04-campaign-summary-prompt-design]
last_updated: 2026-08-04
---

# Think-Block Choice Resolution

A rule surfaced by the [[GoogleAIStudio]] Gemini review of the [[CampaignSummaryPrompt]]: the prompt excludes think blocks (player/AI deliberation) from summaries, yet still wants bullets like "PC decides to investigate X." The reconciliation is that the summarizer should look for the **resolution** of a think block — the CHOICE_ID actually selected — and summarize that decision plus its immediate outcome, discarding the deliberation itself.

In short: deliberation is transcript noise; the committed choice and its consequence are canon. This keeps summaries focused on state changes (what the [[SignificanceThreshold]] governs) rather than on option-weighing that never affected the world.