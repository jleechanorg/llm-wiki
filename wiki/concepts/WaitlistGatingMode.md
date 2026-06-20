---
title: "Waitlist Gating Mode"
type: concept
tags: [access-control, authorization, waitlist]
sources: [waitlist-gating-account-switching-flow]
last_updated: 2026-06-20
---

## Definition

Waitlist Gating Mode is a site-wide access control mechanism that restricts the WorldArchitect.AI platform to authorized users only. When enabled, all routes check for active user authorization via `/api/waitlist/status`.

## Enabling

Waitlist mode is enabled via the environment variable `WAITLIST_MODE_ENABLED`:| Value | Result |
|-------|--------|
| `"true"` | Enabled |
| `"1"` | Enabled |
| `"yes"` | Enabled |
| `"on"` | Enabled |
| (not set / other) | Disabled (default) |

## Behavior

When enabled:
1. All routes check for active user authorization via `/api/waitlist/status`
2. Unauthorized authenticated users see the waitlist gate card
3. Users can click "Use a different account" to switch Google accounts
4. Backend uses `is_waitlist_mode_enabled()` and `get_waitlist_access_status()` in Firestore

## Related Concepts
- [[AccountSwitchingFlow]] — forced account selection
- [[SequenceGuardedCallbacks]] — race condition prevention
- [[SPARouting]] — SPA route wakeup
