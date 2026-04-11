---
title: "PR #472: Add comprehensive Dragon Knight and BG3 Astarion integration tests"
type: source
tags: []
date: 2025-07-10
source_file: raw/prs-worldarchitect-ai/pr-472.md
sources: []
last_updated: 2025-07-10
---

## Summary
- Add comprehensive integration tests for Dragon Knight campaign (moral choice story)  
- Add BG3 Astarion vampire spawn campaign tests
- Create shared `BaseCampaignIntegrationTest` base class to eliminate code duplication (~60% reduction)
- Fix entity ID validation bug that crashed on special characters in NPC names
- Test character creation, combat encounters, and story progression for both campaigns
- Validate game state tracking and core memories persistence

## Metadata
- **PR**: #472
- **Merged**: 2025-07-10
- **Author**: jleechan2015
- **Stats**: +916/-213 in 8 files
- **Labels**: none

## Connections
