---
name: Aside browser subagents defaulted to the wrong account, causing false "no credentials found" blockers
description: ~/.aside/accounts.json currentAccountId pointed at jleechan@worldarchitect.ai (id 1) instead of jleechan@gmail.com (id 0) — the personal account holding saved banking/crypto login credentials. Every browser-automation subagent inherited the wrong identity and wrongly reported blocked logins as unrecoverable.
type: feedback
bead: bd-wrz
---

# Aside browser subagents defaulted to the wrong account

## Context

During tax-2025 document reconciliation (mission `bd-6oj`), three separate
`agy-pair-coder` subagents were dispatched to check Gemini, Scotiabank, and
Morgan Stanley for 2025 documents/activity via Aside browser automation. Two
of the three (Gemini, Morgan Stanley) reported "no accessible credentials
found anywhere — Keychain, autofill, existing tabs all empty" and treated
this as a hard, unrecoverable blocker requiring the user to log in manually.

The user flagged: "you keep using the wrong aside user use jleechan@gmail.com".

## Root cause

`~/.aside/accounts.json` has a `currentAccountId` field selecting which of
two linked Google identities Aside operates as:
- `id: 0` → `jleechan@gmail.com` — the personal identity with saved
  credentials/autofill for personal-context sites (banking, crypto exchange).
- `id: 1` → `jleechan@worldarchitect.ai` — a work identity, no saved personal
  banking/crypto credentials.

`currentAccountId` was set to `1`. Every Aside browser session the subagents
opened therefore ran under the work identity's browser profile, which has no
saved password-manager entries for Gemini or Morgan Stanley — hence the
"no credentials found" reports. Those reports were technically true (no
credentials WERE found under the active profile) but the underlying premise
(that no credentials exist anywhere for this user) was false — they existed
under the correct, inactive profile.

## FIX applied 2026-08-16

`~/.aside/accounts.json`: `currentAccountId` changed `1` → `0`.
Backup preserved at `~/.aside/accounts.json.bak-2026-08-16-before-account-switch`
before the edit (original also carried `currentAccountId: 1`, for revert if
this profile switch has unintended side effects elsewhere).

## Verification

Not yet re-run against Gemini/Morgan Stanley post-fix at time of writing —
the user separately confirmed logging into Morgan Stanley manually in the
interim ("i just logged in to morgan stanley we def have stuff"), corroborating
that the account is active and does have data, independent of this fix.

## Pattern for future browser-automation subagent prompts

Any prompt that dispatches an Aside-browser subagent for a **personal**
context (banking, personal email, personal accounts) should either:
1. State explicitly which Aside account/profile the task expects
   (`jleechan@gmail.com` for personal-context tasks), or
2. Instruct the subagent to check `~/.aside/accounts.json`'s
   `currentAccountId` / list available Aside accounts and confirm it matches
   the expected identity BEFORE concluding "no credentials found" — a
   same-instance "no credentials" finding without checking which profile is
   active is a false negative, not a real blocker.

**Why:** the failure mode is silent and looks identical to a genuine
"user never saved these credentials" case — both present as an empty
autofill/Keychain search. Without checking the active profile identity
first, an agent cannot distinguish "genuinely no saved credentials" from
"wrong profile active."

**How to apply:** add an explicit account-identity check as step 0 of any
Aside-browser subagent prompt touching personal accounts, per this session's
corrected prompt pattern.
