---
title: "PR 7226 Time-Rewind Root Cause (GodModeAgent world_time regression)"
type: source
tags: ["world-time", "gemini-3", "temporal-consistency", "worldarchitect-ai", "pr-7226"]
date: 2026-06-05
source_file: project_2026-06-05_pr7226_time_rewind_root_cause.md
---

## Summary
For campaign `i9xdU7P2bNoMpGqfLBHe`, the time-travel failure is not only session-header enrichment drift — GodModeAgent emitted backward `world_time` and warning-only validation persisted it because monotonicity used `strict=False`.

## Key Claims
- Time regression from `150 AF, February 14, 06:45` to `150 AF, February 11, 11:44`
- Server logged 'Time regression detected' but persisted — strict=False
- Bead rev-lzpla; issue https://github.com/jleechanorg/worldarchitect.ai/issues/7307
- Fix prompt/schema first; then narrow pre-persistence backend invariant to reject regressive world_time without explicit rewind authorization

## Key Quotes
> Future PR 7226 or temporal-consistency work must not overclaim header repair as fixing full narrative/state rewinds

## Connections
- [[TemporalConsistency]] — broader concept
- [[PromptStability]] — fix prompt first per RCF
