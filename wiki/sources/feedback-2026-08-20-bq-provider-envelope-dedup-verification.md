---
title: "Verify campaign-bible deduplication from decoded BQ payloads"
type: source
tags: [worldarchitect-ai, bigquery, gemini, campaign-bible, verification]
date: 2026-08-20
source_file: raw/feedback_2026-08-20_bq-provider-envelope-dedup-verification.md
---

## Summary

PR #9153 removed the Turn-0 story-history copy of campaign lore, retaining the
canonical value in `game_state.custom_campaign_state.god_mode.description`.
The live verification for campaign `ArYA47Fvx8HTYC8jpleO` passed only after
decoding Gemini's provider envelope and its embedded gameplay JSON. The
canonical 180,126-character description occurred once in decoded payload
strings and zero times in decoded `story_history`.

## Key Claims

- Use `worldarchitecture-ai.llm_forensics.llm_payloads` and select the intended
  gameplay `request_json` row; `log_events` is not the raw request corpus.
- Gemini `request_json` is an envelope: the model-bound payload is JSON text in
  `contents[0].parts[0].text` and must be parsed before counting values.
- Counting escaped raw JSON bytes can falsely report duplication because of
  newline or Unicode escaping.
- Preserve the raw row, decoded gameplay payload, and count report so the
  conclusion remains independently reviewable.

## Key Quotes

> "Parse that text before measuring duplication. Do not count raw escaped bytes."

> "Its decoded payload contained that value exactly once across all string fields and zero times in `story_history`."

## Connections

- [[CampaignBibleDuplication]] — the underlying prompt-size regression and its
  canonical single-source model.
- [[GeminiImplicitCachePrefixMeasurement]] — related payload-structure and
  caching investigation.
- [[PR #9153]] — the implementation that removed the Turn-0 duplicate.
