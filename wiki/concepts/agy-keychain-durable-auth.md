---
title: "agy Keychain-Durable Auth"
type: concept
tags: [agy, antigravity, keychain, auth]
date: 2026-07-11
sources:
  - sources/feedback-2026-07-11-agy-keychain-durable-no-fresh-login.md
---

# agy Keychain-Durable Auth

The agy CLI (Google Antigravity) stores its durable OAuth credential in macOS Keychain under service "Antigravity Safe Storage", account "Antigravity Key". Unlike the file-based token in ~/.gemini/oauth_creds.json (which can be corrupted, including the self-referential-symlink bug rev-an94i documented), the Keychain entry is auto-refreshed by every agy invocation and never expires under normal usage.

## Why it matters for agents

Agents working with worldarchitect.ai's agy provider integration frequently encounter the false-positive pattern:
1. Some game-server code path fails with "Authentication required" or "agy authentication required or timed out".
2. Agent (incorrectly) attributes this to a missing/expired token.
3. Agent recommends the user run an interactive `agy` login, which (a) is unnecessary -- the Keychain token is fine, and (b) can in the worst case reset or overwrite the durable Keychain credential.

The actual cause is almost always a file-side problem (corrupt symlink, missing runtime HOME, broken install.sh state), NOT an auth failure. The fix is `rm ~/.gemini/oauth_creds.json` + re-run `install.sh`, NOT a fresh login.

## Corrective probe (in priority order)

1. `security find-generic-password -s "Antigravity Safe Storage" -a "Antigravity Key" -w` -- non-empty?
2. `HOME=/tmp/agy-clean-home-v1 agy --print --new-project --sandbox --prompt "Reply with just the word pong"` -- returns a model response?
3. Only if both fail should non-login fixes be tried: rm broken symlink, reinstall, retry.
4. Only if all of those still fail, escalate to "needs interactive login" -- and even then, never use a path that overwrites the durable Keychain entry without explicit user consent.

## Related

- [[Feedback20260710AgyProviderDefaultOnStaleBelief]] -- inverse pole of the same failure class
- Source: [[feedback-2026-07-11-agy-keychain-durable-no-fresh-login]]
