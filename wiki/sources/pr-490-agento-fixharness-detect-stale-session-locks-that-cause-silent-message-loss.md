---
title: "[agento] fix(harness): detect stale session locks that cause silent message loss"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-04
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/490
pr_number: 490
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background

2026-04-04: OpenClaw stopped responding to Slack DMs for ~6 hours. Gateway reported HTTP 200 and all 6 canary checks passed. Root cause: pid=59865 (a dead agent subprocess) held stale `.lock` files in `agents/main/sessions/`, causing every inbound message to hit `"session file locked (timeout 10000ms)"` and be silently dropped.

## Goals

Make this failure class detectable before it causes an outage — at canary time, at doctor time, and via documented diagnosis procedure.

## Tene...

## Key Changes
- 1 commit(s) in this PR
- 3 file(s) changed

- Merged: 2026-04-04

## Commit Messages
1. fix(harness): detect stale session locks that cause silent message loss
  
  Root cause of 2026-04-04 outage: dead process held .lock files in
  agents/main/sessions/, causing all Slack messages to timeout silently
  while gateway HTTP health reported 200/live.
  
  Harness fixes (3 layers):
  - staging-canary.sh: add check 7 — scan for dead-owner session locks
  - doctor.sh: add Session health section — stale locks + .tmp accumulation
  - CLAUDE.md: document session lock silent failure + detection/fix procedure
  
  Canary now 7/7. Will catch this failure class before any deploy or
  immediately via doctor/monitor runs.
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

## Files Changed
- `CLAUDE.md`
- `scripts/doctor.sh`
- `scripts/staging-canary.sh`

## Review Notes
1. @coderabbitai all good?

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **5...

3. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions`[bot] I'll take a look at the PR now!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is appl...

4. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, CI checks, and comments
gh pr view 490 --repo jleechanorg/jleechanclaw -...

6. @coderabbitai approve

7. @coderabbitai all good?

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get latest PR status, CI checks, comments, and commits
gh pr view 490 --repo jleechanor...

9. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Comments resolved and changes approved.

</details>

10. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

