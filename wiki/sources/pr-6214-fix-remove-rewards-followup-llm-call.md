---
title: "PR #6214: fix: remove rewards followup LLM call"
type: source
tags: [worldarchitect.ai, rewards, llm-call, optimization, atomicity]
date: 2026-04-11
source_file: raw/worldarchitect.ai/pr-6214.md
---

## Summary
Removes the second LLM call (`_process_rewards_followup`) that was added as a defensive safety net after the primary narrative call. The primary LLM receives `rewards_pending` in game state and is instructed via prompts to include `rewards_box` directly. No second call is needed — if rewards are pending, the primary response MUST include them.

## Key Claims
- Primary LLM with `rewards_pending` instruction is sufficient for rewards_box inclusion
- Second followup call is redundant and adds latency
- Removing it simplifies the rewards pipeline

## Root Cause
The followup existed because the LLM sometimes failed to include `rewards_box` despite prompt instructions.

## Connections
- [[RewardsBox]] — the JSON structure being processed
- [[DeferredRewardsProtocol]] — protocol for deferred rewards
- [[rewards_box/atomicity]] — related to the rewards_box/planning_block atomicity fixes

## Changed Files
- 6 files changed (+416/-282)
