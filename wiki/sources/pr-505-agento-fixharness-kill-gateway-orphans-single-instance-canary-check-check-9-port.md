---
title: "[agento] fix(harness): kill gateway orphans + single-instance canary check (check 9, port-filtered)"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-05
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/505
pr_number: 505
pr_repo: jleechanorg/jleechanclaw
---

## Summary
### Background
2026-04-05 incident: immediately after a successful deploy (8/8 canary PASS), OpenClaw went completely dark. 3 \`openclaw-gateway\` processes competed for \`sessions.json.lock\` → WS pong starvation → total HTTP unresponsiveness (curl exit 28).

Root cause: \`deploy.sh\` Stage 4 used \`launchctl stop\` + \`launchctl start\` without killing orphaned processes not tracked by launchd. Multiple instances can coexist on the same state dir silently past the old 8-check canary.

### Goal...

## Key Changes
- 5 commit(s) in this PR
- 4 file(s) changed

- Merged: 2026-04-05

## Commit Messages
1. [agento] feat: add ZFC rule to agentRules in agent-orchestrator.yaml
2. [agento] fix: escape embedded double quotes in YAML scalar
3. [agento] fix: add ZFC rule to all project agentRules overrides (cursor[bot] review)
4. [agento] fix(harness): kill gateway orphans + single-instance canary check (check 9)
  
  Post-deploy lock storm: 3 openclaw-gateway processes competed for sessions.json.lock
  causing WS pong starvation and total HTTP unresponsiveness (2026-04-05 incident).
  
  Root cause: deploy.sh Stage 4 used launchctl stop+start without killing orphaned
  processes not tracked by launchd. Multiple instances coexist on same state dir.
  
  Fixes:
  - deploy.sh Stage 4: kill all openclaw-gateway orphans before restart, clear stale
    locks, assert exactly 1 process after startup (hard failure if count != 1)
  - staging-canary.sh: add check 9 — single-instance assertion (9/9 pass = clean)
  - CLAUDE.md: document single-instance mandate + 2026-04-05 root cause
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. fix(canary): check 9 must filter by port, not count all gateway processes
  
  The pgrep-based count falsely fails when both staging (18810) and
  prod (18789) gateways are running — it counts both as orphans.
  
  Fix: use lsof -i :PORT -sTCP:LISTEN | awk '{print $2}' | sort -u
  to count unique PIDs listening on the target port only.
  
  Also fix: deduplicate IPv4+IPv6 fds from same process.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `CLAUDE.md`
- `agent-orchestrator.yaml`
- `scripts/deploy.sh`
- `scripts/staging-canary.sh`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **6...

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get the diff of the PR to review the changes
git diff HEAD~1 HEAD -- scripts/deploy.sh ...

4. @coderabbitai review

5. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions` Yes, all good! My earlier review covered the full diff — here's the quick summary:

- ✅ **No blocking issues** found. The root-cause fix is correct and p...

8. @coderabbitai review

9. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

10. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, CI checks, merge status, and comments
gh pr view 505 --repo jleechanorg/...

12. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | FAIL | state=none...

13. @coderabbitai review

14. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

15. @coderabbitai review

16. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

