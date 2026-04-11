---
title: "fix: replace hardcoded paths with HOME for portability"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-09
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/538
pr_number: 538
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary
Replace hardcoded `/Users/jleechan` paths with `$HOME` in 6 scripts for multi-user portability.

## Changes
- `stability-report.launchd.sh`: /Users/jleechan/.openclaw → $HOME/.openclaw
- `simplify-daily.sh`: /Users/jleechan/project_agento → $HOME/project_agento
- `orch-7b7-slack-check.sh`: /Users/jleechan/.worktrees → $HOME/.worktrees
- `openclaw-upgrade-safe.sh`: NVM paths → $HOME
- `mem0-native-module-watchdog.sh`: NVM paths → $HOME
- `install-openclaw-launchd.sh`: NVM path → $HOME...

## Key Changes
- 1 commit(s) in this PR
- 6 file(s) changed

- Merged: 2026-04-09

## Commit Messages
1. fix: replace hardcoded /Users/jleechan with $HOME for portability
  
  - scripts/stability-report.launchd.sh: /Users/jleechan/.openclaw → $HOME/.openclaw
  - scripts/simplify-daily.sh: /Users/jleechan/project_agento → $HOME/project_agento
  - scripts/orch-7b7-slack-check.sh: /Users/jleechan/.worktrees → $HOME/.worktrees
  - scripts/openclaw-upgrade-safe.sh: NVM paths → $HOME
  - scripts/mem0-native-module-watchdog.sh: NVM paths → $HOME
  - scripts/install-openclaw-launchd.sh: NVM path → $HOME

## Files Changed
- `scripts/install-openclaw-launchd.sh`
- `scripts/mem0-native-module-watchdog.sh`
- `scripts/openclaw-upgrade-safe.sh`
- `scripts/orch-7b7-slack-check.sh`
- `scripts/simplify-daily.sh`
- `scripts/stability-report.launchd.sh`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **3...

2. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #538: [fix: replace hardcoded paths with HOME for portability](https://github.com/jleechanorg/jleechanclaw/pull/538) — claims to replace hardcoded `/Users/jleechan` and NV...

3. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR details including reviews, state, and body
gh pr view 538 --repo jleechanorg/jleechanclaw --json title,body,state,reviews,reviewDecision,files

echo "--- ...

