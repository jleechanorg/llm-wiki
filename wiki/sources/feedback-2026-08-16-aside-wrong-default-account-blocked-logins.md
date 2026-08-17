---
title: "Aside browser subagents defaulted to the wrong account, blocking real logins"
type: source
tags: [aside, browser-automation, tooling-bug, tax-2025]
date: 2026-08-16
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-Downloads-tax-2025/memory/feedback_2026-08-16_aside_wrong_default_account_blocked_logins.md
---

## Summary

During tax-2025 document reconciliation, Aside-browser subagents dispatched to check Gemini and Morgan Stanley for 2025 documents reported "no accessible credentials found anywhere" and treated it as an unrecoverable blocker. The real cause: `~/.aside/accounts.json`'s `currentAccountId` was set to `1` (`jleechan@worldarchitect.ai`, a work identity with no saved personal banking/crypto credentials) instead of `0` (`jleechan@gmail.com`, which holds the actual saved credentials). Every subagent inherited the wrong active profile. Fixed by changing `currentAccountId` to `0`, with a backup preserved before the edit.

## Key Claims

- A "no credentials found" report from a browser-automation subagent can be a false negative caused by the wrong active account/profile, not proof that no credentials exist for the user at all.
- `~/.aside/accounts.json` supports multiple linked Google identities (`accounts[]`) and a single `currentAccountId` that determines which profile's saved passwords/autofill are visible to any Aside session opened at that time.
- The failure mode is silent: an empty Keychain search + empty autofill under the wrong profile looks identical to genuinely-never-saved credentials.

## Key Quotes

> "you keep using the wrong aside user use jleechan@gmail.com" — user correction that triggered the root-cause investigation

## Connections

- [[jeffrey-oracle]] — personal financial account access pattern; relevant to any future browser-automation task touching jleechan's personal (not work) identity.
- [[aside-browser-default]] — the skill governing Aside-as-primary-browser policy; this finding is a gap in that skill's guidance (doesn't mention multi-account profile selection).
