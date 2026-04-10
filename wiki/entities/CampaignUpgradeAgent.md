---
title: "CampaignUpgradeAgent"
type: entity
tags: [worldarchitect, agent, campaign-upgrade]
sources: []
last_updated: 2026-04-08
---

Special agent mode in WorldArchitect.AI that handles campaign tier upgrades (mortal→divine→sovereign). When this agent mode is active, the system enforces presentation of an ascension ceremony choice to the player. If the LLM fails to provide the choice, server-side helpers inject a minimal choice to ensure the player can proceed with their upgrade.

**Associated Code**: `inject_campaign_upgrade_choice_if_needed()` in planning block helpers
