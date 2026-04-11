---
title: "[P1] fix(launchd): ao7green copy scripts to OPENCLAW_HOME + migrate gateway cron"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-06
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/522
pr_number: 522
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary
Follow-up to merged https://github.com/jleechanorg/jleechanclaw/pull/521

## Changes
- **install-launchagents.sh**: Copy `ao7green-pr-monitor*.sh` into `~/.openclaw/scripts/` before loading the LaunchAgent (fresh installs / non-`~/.openclaw` worktrees).
- **install-openclaw-scheduled-jobs.sh**: Add gateway cron job `64f2399d-33f4-4451-be87-05350d2b2590` to `MIGRATED_JOBS` so `install-openclaw-scheduled-jobs.sh` disables it when migrating.
- **install-launchagents.sh**: After installin...

## Key Changes
- 2 commit(s) in this PR
- 3 file(s) changed

- Merged: 2026-04-06

## Commit Messages
1. feat(launchd): add ao7green-jleechanclaw 30-min schedule plist
  
  - Add ai.openclaw.schedule.ao7green-jleechanclaw.plist (StartInterval: 1800s)
  - Runs ao7green-pr-monitor.launchd.sh against jleechanorg/jleechanclaw
  - Posts to #ai-slack-test (C0AKALZ4CKW) same as gateway cron predecessor
  - Add install-plist call in install-launchagents.sh
  - Persists across gateway restarts (gateway cron was killing the 30m loop)
2. fix(launchd): copy ao7green scripts, migrate gateway cron, avoid duplicate logs
  
  - install-launchagents: copy ao7green monitor scripts to OPENCLAW_HOME before load
  - install-openclaw-scheduled-jobs: add 64f2399d cron id to MIGRATED_JOBS
  - plist: StandardOutPath /dev/null (tee already writes AO_MONITOR_LOG)
  
  Made-with: Cursor

## Files Changed
- `launchd/ai.openclaw.schedule.ao7green-jleechanclaw.plist`
- `scripts/install-launchagents.sh`
- `scripts/install-openclaw-scheduled-jobs.sh`

## Review Notes
1. @coderabbitai all good?

2. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #522: [P1] fix(launchd): ao7green copy scripts to OPENCLAW_HOME + migrate gateway cron — claims to copy ao7green-pr-monitor scripts to OPENCLAW_HOME and migrate the gatewa...

3. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **3...

4. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Yes, the code changes look solid from a review standpoint. Here's my assessment:

**✅ plist** — Redirecting `StandardOutPath` to `/dev/null` is correct; ...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — The Skeptic FAIL here is an **infrastructure failure**, not a code gap. The Codex agent hit its usage quota and couldn't complete the analysis, so the FA...

6. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, CI checks, and comments
gh pr view 522 --repo jleechanorg/jleechanclaw -...

8. ## Evidence
Verified configuration and tests on branch `feat/ao7green-jleechanclaw-launchd`:

1. **Plist Linting**:
```bash
plutil -lint launchd/ai.openclaw.schedule.ao7green-jleechanclaw.plist
# Output: /Users/jleechan/.worktrees/jleechanclaw/jc-1707/launchd/ai.openclaw.schedule.ao7green-jleechancl...

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check the actual review states on PR `#522`
gh pr view 522 --repo jleechanorg/jleechanc...

10. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=8 |\n| 2. No conflicts | PASS | already merged |\n| 3. CR approved | PASS | state=APPROVED |\n| 4. Bug...

