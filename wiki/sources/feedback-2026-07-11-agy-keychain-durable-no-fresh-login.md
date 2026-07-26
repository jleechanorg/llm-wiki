---
title: "agy auth is durable in macOS Keychain; never recommend interactive login before verifying"
type: source
tags: [agy, antigravity, keychain, auth, worldarchitect, feedback, anti-pattern]
date: 2026-07-11
source_file: feedback_2026-07-11_agy_keychain_durable_no_fresh_login.md
---

## Summary
Worldarchitect.ai agents repeatedly assume agy needs a fresh interactive login when the user's actual auth state is durable in macOS Keychain. The user's mental model ("I shouldn't need to login again for the millionth time") is correct: Keychain entry "Antigravity Safe Storage / Antigravity Key" holds a live token (prefix tUMw343RdbqsSwC3EYPlmQ==), and a clean-HOME agy --print returns real model output without any login flow. The earlier failure was a broken self-referential symlink at ~/.gemini/oauth_creds.json -- which agy --print doesn't read (CLI reads Keychain). Two TTY traps to avoid: treating agy account list's bubbletea-UI TTY error as proof agy --print is broken, and recommending a fresh login that can reset the durable Keychain credential.

## Key Claims
- agy auth is durable in macOS Keychain under service "Antigravity Safe Storage", account "Antigravity Key"; no interactive login needed.
- The earlier "Authentication required" failure was caused by a broken self-referential symlink at ~/.gemini/oauth_creds.json, not by an auth failure.
- This is the OPPOSITE pole of feedback_2026-07-10_agy_provider_default_on_stale_belief.md (which captured defaulting agy OFF without verifying); same root cause class: agent confabulated state without probing.
- Corrective probe (priority order): (1) security find-generic-password, (2) clean-HOME agy --print --prompt pong, (3) only if both fail, try non-login fixes (rm symlink + install.sh), (4) only if all fail, escalate to login.

## Key Quotes
> "macOS Keychain entry 'Antigravity Safe Storage / Antigravity Key' holds token prefix tUMw343RdbqsSwC3EYPlmQ==; live agy --print --prompt pong returned real model output without any login flow"

> "The earlier failure (agy_provider: agy authentication required or timed out) was caused by a broken self-referential symlink at ~/.gemini/oauth_creds.json -- a file-level corruption that agy --print doesn't even read"

## Connections
- [[Feedback20260710AgyProviderDefaultOnStaleBelief]] — inverse pole of the same failure class (defaulting OFF vs defaulting ON with no probing)
- [[RevY2buf]] — bead that was closed with corrected framing after this verification
- [[Rev9ce1b]] — bead tracking the install.sh symlink guard gap, now closed via PR #8334
- [[RevAn94i]] — root-cause bead documenting the self-referential symlink bug
