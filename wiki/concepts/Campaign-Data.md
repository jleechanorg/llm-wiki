---
title: "Campaign Data"
type: concept
tags: [data, campaign, game-state]
sources: [ai-content-personalization-integration-test]
last_updated: 2026-04-08
---

## Overview
User-provided data defining a campaign's unique characteristics. Includes title, character name, setting description, and campaign type. Used to personalize AI-generated stories.

## Key Fields
- `title` — campaign title
- `character_name` — main character name
- `setting` — world/realm description
- `description` — additional context
- `campaign_type` — type of campaign (e.g., Custom Adventure)

## Related Pages
- [[AI Content Personalization Integration Test]] — tests usage of this data
- [[GameState]] — carries campaign_data through the system
