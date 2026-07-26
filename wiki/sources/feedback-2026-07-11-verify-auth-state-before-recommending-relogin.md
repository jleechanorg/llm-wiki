---
title: "Verify auth state with two probes before recommending re-login"
type: source
tags: [auth, login, keychain, antigravity, worldarchitect, feedback, anti-pattern, process-improvement]
date: 2026-07-11
source_file: feedback_2026-07-11_verify_auth_state_before_recommending_relogin.md
---

## Summary
Quantitative audit of the "agent forces user to re-login" pattern across 8,640 Claude Code sessions / 38 MB of assistant text: 11 hits total, all concentrated in the last 2 days and almost entirely in the agy/agx/Keychain domain. Pattern is NOT random noise — a concentrated cluster where the same wrong conclusion gets repeated via relayed transcripts, beads, memory reads.

## Key Claims
- 11/8640 = 0.13% historical rate, but concentrated: every hit last 2 days, every hit agy/agx/Keychain.
- Agents collapse several narrow signals (`agy account list` TTY error, missing `oauth_creds.json`, sandbox HOME without token file) into a false-positive "needs re-login".
- Corrective probe: (1) `security find-generic-password` for the tool's Keychain entry; (2) cheap non-UI invocation. Only escalate re-login if both fail.

## Connections
- [[Feedback20260710AgyProviderDefaultOnStaleBelief]] — inverse pole
- [[Feedback20260711AgyKeychainDurableNoFreshLogin]] — agy-specific instance
