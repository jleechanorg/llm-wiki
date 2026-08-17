---
title: "MaxOAuthSubscription"
type: concept
tags: [claude-code, billing, max, oauth]
last_updated: 2026-08-12
---

# Max OAuth Subscription

Claude Max is Anthropic's subscription plan with two tiers: Max 5x ($100/mo) and Max Pro 20x ($200/mo). When `hasExtraUsageEnabled=false` (the default), usage beyond the included quota results in hard limits, not overage billing.

**Detection signals:**
- `~/.claude.json` → `oauthAccount.billingType = "stripe_subscription"`, `organizationType = "claude_max"`, `organizationRateLimitTier = "default_claude_max_20x"` (or `default_claude_max_5x`)
- `~/.claude/.credentials.json` → `claudeAiOauth.subscriptionType = "max"`, `rateLimitTier = "default_claude_max_20x"`
- `~/.claude.json` → `passesEligibilityCache` block (OAuth-flow metadata: referral codes, share links)
- bashrc explicitly `unset ANTHROPIC_API_KEY` and `unset ANTHROPIC_BASE_URL` so default `claude` invocation falls through to OAuth

**Rate limits:** 5-hour and 7-day rolling windows. Per-model caps also exist (e.g., Opus has its own limit).

**Sources:** [[feedback-2026-08-12-token-burn-investigation-learnings]], [[feedback-2026-08-12-route-classifier-claudem-vs-max]], anthropics/claude-code docs.