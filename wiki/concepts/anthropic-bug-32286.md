---
title: "AnthropicBug32286"
type: concept
tags: [claude-code, billing, anthropic-bug, credentials, watch]
last_updated: 2026-08-12
---

# Anthropic Bug #32286 — Silent API Billing Mode

Documented at [anthropics/claude-code#32286](https://github.com/anthropics/claude-code/issues/32286).

**The bug:** If `~/.claude/.credentials.json` `claudeAiOauth.subscriptionType` or `rateLimitTier` becomes null, the Claude Code CLI silently enters API billing mode and charges usage credits EVEN when the user is on a Max subscription. This bypasses the `hasExtraUsageEnabled=false` flag and can result in unexpected charges.

**Trigger conditions:**
- `~/.claude/.credentials.json` becomes corrupted
- CLI upgrade that changes auth schema
- Re-authentication that fails partway through
- Manual edit of credentials file

**Detection:**
```bash
python3 -c "
import json
with open('$HOME/.claude/.credentials.json') as f:
    d = json.load(f)
oa = d.get('claudeAiOauth', {})
print('subscriptionType:', oa.get('subscriptionType'))
print('rateLimitTier:', oa.get('rateLimitTier'))
# BUG ACTIVE if either is null
"
```

**User's status (verified 2026-08-12):** `subscriptionType="max"`, `rateLimitTier="default_claude_max_20x"` — bug NOT active.

**Recommended hook:** Alert when either field becomes null. Bead: `jleechan-6iu` (P3, covers related claudem auto-route hook; credentials-null watch is a separate future bead).

**Sources:** [[feedback-2026-08-12-token-burn-investigation-learnings]], anthropics/claude-code GitHub issue #32286, /research finding 2026-08-12.