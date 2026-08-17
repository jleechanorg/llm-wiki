---
title: "Transcript Chunking for Iterative Summarization"
type: concept
tags: [summarization, chunking, long-context, prompt-engineering, pipeline]
sources: [2026-08-04-campaign-summary-prompt-design]
last_updated: 2026-08-04
---

# Transcript Chunking for Iterative Summarization

[[ChatGPT]]'s scaling concern about the [[CampaignSummaryPrompt]]: very long campaign transcripts exceed what one summarization pass can process, so the prompt should include instructions for **handling partial transcripts and iterative summarization** — process in segments, then merge, while preserving the strict chronological ordering guarantee across segment boundaries.

Related suggestion: optional per-bullet sequence identifiers or timestamps as output metadata, which make merged multi-segment summaries referenceable and ordering-verifiable. This mirrors the batch-ingestion pattern this wiki already uses for multi-thousand-entry campaigns, where per-segment processing is the only viable path.