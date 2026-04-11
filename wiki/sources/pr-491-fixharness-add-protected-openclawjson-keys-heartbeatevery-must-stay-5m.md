---
title: "fix(harness): add protected openclaw.json keys — heartbeat.every must stay 5m"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-04
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/491
pr_number: 491
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background

On 2026-04-04, an agent changed agents.defaults.heartbeat.every from 5m to 30m in ~/.openclaw/openclaw.json. This caused doctor.sh to FAIL on every monitor run and the monitor-agent to report STATUS=PROBLEM. The constraint existed only in doctor.sh — no agent instruction stated the value was protected.

Root cause (from /harness analysis): agents mutate openclaw.json without knowing which keys doctor.sh validates. The constraint knowledge was absent from any file agents read befor...

## Key Changes
- 1 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-04

## Commit Messages
1. fix(harness): add protected openclaw.json keys table to CLAUDE.md
  
  Agents changed agents.defaults.heartbeat.every to 30m (2026-04-04 incident),
  causing monitor STATUS=PROBLEM every hourly cycle. The constraint existed only
  in doctor.sh — no agent instruction prevented the change.
  
  Add a protected keys table directly in the openclaw.json mutation safety section
  listing all doctor.sh-enforced values as immutable without explicit user approval.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `CLAUDE.md`

## Review Notes
1. @coderabbitai all good?

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **1...

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check the PR `#491` details, status, and diff
gh pr view 491 --repo jleechanorg/jleecha...

4. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=8 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | FAIL | state=none...

5. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

