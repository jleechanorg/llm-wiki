---
title: "PR #6420: ZFC level-up schema prerequisites + validation hardening"
type: source
tags: [zfc, level-up, M0-cleanup, schema, validation]
date: 2026-04-21
source_file: /Users/jleechan/roadmap/zfc-pr-task-specs-2026-04-22.md
---

## Summary
PR #6420 is the M0 / Stage 0 cleanup lane for the ZFC level-up migration. It removes a duplicate direct early-projection call from `llm_parser.py`, narrows Stage 0 wiring tests to M0-safe ownership and fallback characterization, and adds responsibility headers for touched ZFC files.

## Key Claims
- `_build_early_metadata_payload(...)` is the single early projection owner in `mvp_site/llm_parser.py`
- Legacy generic-planning-block fallback is characterized, not silently deleted
- Prompt/tool contract hash refreshed for touched schema file
- CI green at SHA 019ed3330

## Key Quotes
> "This PR is the **M0 / Stage 0 cleanup-first lane only** for the level-up ZFC migration. Explicitly out of scope: future-state resolver ownership enforcement, broad architecture cleanup, prompt/schema renaming rollout, `new_level` compatibility/schema expansion work"

## Connections
- [[Level-Up Bug Chain]] — relates to ZFC level-up cleanup chain
- [[Normalization Atomicity]] — early projection canonicalization touches
- [[ZFC PR Task Specs]] — canonical execution surface for 8 follow-on lanes
