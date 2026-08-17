---
title: "Significance Threshold (campaign summarization)"
type: concept
tags: [summarization, prompt-engineering, granularity, inclusion-criteria]
sources: [2026-08-04-campaign-summary-prompt-design]
last_updated: 2026-08-04
---

# Significance Threshold

The central underspecified term in the [[CampaignSummaryPrompt]]: which transcript events are "significant" enough to earn a summary bullet. All three reviewers flagged it independently.

- **[[ChatGPT]]**: set a minimum-impact guideline (e.g. XP awards, mission completions) to prevent overly granular bullets.
- **[[GoogleAIStudio]] Gemini**: optionally define it explicitly — "narrative impact, changes to core character power/status, or advancement of primary plotlines" — though good examples may suffice.
- **[[Cursor]] Gemini**: add a fallback — "If an event's significance is ambiguous, err on the side of including it" — since the goal is capturing all potentially pivotal moments.

The tension: too low a threshold reproduces the transcript; too high loses pivotal setup. The err-toward-inclusion fallback biases toward recall over compression, appropriate when the summary feeds downstream ingestion (as in this wiki's campaign pipeline).