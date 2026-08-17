---
title: "MiniMaxMeteredNotFree"
type: concept
tags: [claude-code, billing, minimax, api, anti-pattern]
last_updated: 2026-08-12
---

# MiniMax Is Metered Per-Token, Not Free

MiniMax is a Claude-compatible LLM provider accessed via `https://api.minimax.io/anthropic`. Despite `claude-code-claudem` (`claudem`) being marketed as the "default coding skill" with $0 ccusage cost, **MiniMax charges per-token like any other LLM provider**.

The `MINIMAX_API_KEY` (in `~/.bashrc:290` and current shell env) is a pay-as-you-go API key, not a free-tier key. ccusage shows MiniMax-M3 at $0 only because ccusage lacks MiniMax pricing data — NOT because MiniMax is free.

**Anti-pattern:** "X tool shows Y model at $0" ≠ "Y model is free." Cost = 0 in any aggregator is a missing-data signal until proven otherwise.

**Correct framing:** Routing heavy investigation to claudem shifts spend from Max flat-fee → MiniMax per-token. The right comparison is MiniMax per-token cost vs Max marginal value (the cost of being rate-limited or quota-exhausted on Max), not "is it free?"

**Sources:** [[feedback-2026-08-12-token-burn-investigation-learnings]], `/advice` Reviewer A caught the mistake 2026-08-12.