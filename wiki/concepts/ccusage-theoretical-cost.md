---
title: "CcusageTheoreticalCost"
type: concept
tags: [claude-code, billing, ccusage, anti-pattern]
last_updated: 2026-08-12
---

# Ccusage Theoretical Cost

ccusage's `Cost (USD)` column is calculated from token counts × LiteLLM pricing data, NOT from the Anthropic billing API. Anthropic's own documentation states the JSONL `costUSD` field "may differ from your actual bill."

For Claude Max subscribers, the figure is a theoretical conversion at standard list rates — actual billing is the Max flat fee ($100/mo Max 5x or $200/mo Max Pro 20x). For API key users, the figure approximates what an API user would pay but may not match due to caching discounts, rate reductions, or billing tier differences.

**Cheap check FIRST:** `~/.claude.json` → `oauthAccount.hasExtraUsageEnabled`. If `false`, the user is on Max flat fee and no per-token overage billing is possible.

**Sources:** [[feedback-2026-08-12-token-burn-investigation-learnings]], anthropics/claude-code docs, ccusage GitHub repository.