---
title: "Campaign bible duplication in the LLM payload"
type: concept
tags: [latency, prompt, campaign-bible]
date: 2026-08-18
last_updated: 2026-08-18
---

# CampaignBibleDuplication

On mature nocturne-class campaigns (~545 turns, ~300k prompt tokens) the campaign bible (~180k chars) can appear in three payload channels:

1. `campaign_setting_reference` (hoisted static prefix)
2. `serialized_game_state` via `custom_campaign_state.god_mode.description`
3. `story_context` via `story_history[0]` creation dump

This is the primary **token-count** latency lever (`rev-fl4z6` / [#9061](https://github.com/jleechanorg/worldarchitect.ai/issues/9061)). It is **not** the same claim as “implicit cache is 0%”. After PR 8856, same-agent implicit hits on `SGxsM2xdermqwOmI37SF` clustered near 50% (SI-sized) even with this duplication.

Write-side stop-seed: `rev-taukr`. Prompt-dict filter: `rev-fl4z6.1`. Turn-0 excision for established campaigns: `rev-fl4z6.2`.

See [[GeminiImplicitCachePrefixMeasurement]].
