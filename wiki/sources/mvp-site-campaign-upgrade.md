---
title: "Campaign Upgrade Planning Block Helpers"
type: source
tags: [planning-block, campaign-upgrade, choice-normalization]
sources: []
last_updated: 2026-04-14
---

## Summary

Server-side enforcement for campaign upgrade choice injection into planning_block. When CampaignUpgradeAgent is selected, ensures a "Begin Divine/Sovereign Ascension" choice is presented. Handles normalization of dict-format choices to array format, duplicate injection prevention, and semantic routing gap-filling.

## Key Claims

- **Choice Injection**: Injects upgrade_campaign choice when agent mode is MODE_CAMPAIGN_UPGRADE and upgrade is actually available
- **Dict-to-Array Conversion**: `normalize_planning_block_choices()` converts dict-format choices to list format with ID collision handling
- **Duplicate Prevention**: Checks for existing matching choice by text before injection
- **Priority Logic**: Multiverse upgrade ("Begin Sovereign Ascension") takes priority over divine ("Begin Divine Ascension")
- **ID Collision Handling**: Suffixes duplicate IDs with numeric suffixes up to 1000 attempts

## Key Quotes

> "Server-side enforcement of campaign upgrade choice in planning_block"

> "The LLM should present a choice to begin the ascension ceremony. If missing, inject a minimal choice so the player can proceed"

> "Avoid duplicate injection if a matching choice already exists by text"

## Connections

- [[PlanningBlock]] — planning block structure
- [[CampaignUpgrade]] — upgrade agent mode
- [[DivineAscension]] — divine ascension ceremony
- [[MultiverseAscension]] — sovereign/multiverse ascension

## Contradictions

- None identified