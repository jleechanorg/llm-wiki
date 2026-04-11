---
title: "[agento] fix(canary): add --prefix to npm ls so SDK version is detected correctly"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-05
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/516
pr_number: 516
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary
- Fix check 5 (SDK protocol version) in `staging-canary.sh` — `npm ls` was running from the worktree directory (no node_modules), returning empty and triggering the fail-closed error
- Add `--prefix ~/.openclaw` so `npm ls` resolves from the correct install location
- Also add `~/.openclaw` as a fallback path in the secondary node resolve
- Both staging (port 18810) and prod (port 18789) canaries now pass 9/9

## Test plan
- [x] Worktree version of `staging-canary.sh --port 18810` → 9...

## Key Changes
- 2 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-05

## Commit Messages
1. fix(canary): add --prefix to npm ls so SDK version is detected correctly
  
  staging-canary.sh check 5 (SDK protocol version) was failing because
  npm ls was run from the worktree directory (no node_modules), returning
  empty. Adding --prefix ~/.openclaw resolves from the correct install.
  
  Fixes: both staging (18810) and prod (18789) canaries now pass 9/9.
2. fix(canary): expand tilde in node -e path and fix SDK detection fallback

## Files Changed
- `scripts/staging-canary.sh`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **1...

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Find staging-canary.sh and show relevant changes
fd -i 'staging-canary.sh' --exec cat {...

4. @coderabbitai all good?

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — **Mostly yes, with one minor caveat worth noting:**

✅ **Primary fix** (`npm ls --prefix ~/.openclaw`) is correct and solves the regression. The 9/9 resu...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions` — Yes, mostly all good. Quick summary of the analysis:

- ✅ **Primary fix** (`npm ls --prefix ~/.openclaw`) — correct and working. This is what fixed the...

8. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

9. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #516: [agento] fix(canary): add --prefix to npm ls so SDK version is detected correctly — fixes `staging-canary.sh` check 5 by pointing `npm ls` at `~/.openclaw` instead o...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fetch PR reviews for PR `#516`
gh pr view 516 --repo jleechanorg/jleechanclaw --json re...

11. @coderabbitai all good?

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Not quite "all good" yet — here's the current state:

| Item | Status |
|---|---|
| Primary fix (`npm ls --prefix ~/.openclaw`) | ✅ Correct, confirmed by...

13. ## Evidence Review — VERDICT: PASS

**Evidence Bundle**: None (ops/chore PR — minimal evidence standard applies)

---

### Diff Review

Single-file change to `scripts/staging-canary.sh` — 4 additions, 3 deletions.

**Change 1**: `npm ls @agentclientprotocol/sdk --prefix "$HOME/.openclaw"`
- `--prefi...

14. PR is green (7/7 criteria met — awaiting auto-merge)

| Gate | Result |
|------|--------|
| 1 CI green | PASS |
| 2 No conflicts | PASS |
| 3 CR approved | PASS |
| 4 Bugbot clean | PASS |
| 5 Comments resolved | PASS |
| 6 Evidence format | WARN (skeptic acceptable for ops/chore PR) |
| 7 Skeptic P...

15. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, CI checks, reviews, and merge state
gh pr view 516 --repo jleechanorg/jl...

