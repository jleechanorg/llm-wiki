---
title: "Server-Side Choice Injection"
type: concept
tags: [worldarchitect, game-logic, agent-enforcement]
sources: []
last_updated: 2026-04-08
---

Pattern where the server automatically injects missing UI choices when a specific agent mode is active. In this case, when `MODE_CAMPAIGN_UPGRADE` is detected but the LLM didn't provide an ascension choice, the system injects a minimal choice ("Begin Divine Ascension" or "Begin Sovereign Ascension") so the player can proceed.

This ensures critical gameplay paths aren't blocked by LLM behavior variance.
