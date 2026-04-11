---
title: "PR #5700: Enforce living world scene visibility in prompts"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldarchitect-ai/pr-5700.md
sources: []
last_updated: 2026-02-22
---

## Summary
- Enforce living world scene visibility in prompts so `scene_event` must appear in player narrative on the same turn.
- Require discovered `world_events` that have player-facing impact to be reflected in narrative language.
- Fix `process_action_unified` to include `processing_metadata` (with `raw_request_payload`) in the unified response when `include_raw_llm_payloads=True` was set — previously the dict was never copied into the response, causing LLM context tests to fail.
- Add `world_events`

## Metadata
- **PR**: #5700
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +315/-161 in 9 files
- **Labels**: none

## Connections
