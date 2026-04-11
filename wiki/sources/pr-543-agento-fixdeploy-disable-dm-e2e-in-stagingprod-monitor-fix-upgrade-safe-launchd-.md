---
title: "[agento] fix(deploy): disable DM e2e in staging+prod monitor; fix upgrade-safe launchd label; fix mem0 log msg"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-11
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/543
pr_number: 543
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary

- **deploy.sh**: Add `OPENCLAW_MONITOR_SLACK_E2E_MATRIX_ENABLE=0` for both staging and prod monitor runs — DM e2e tests fail when both gateways share the same socket-mode app token (Slack routes DMs to whichever grabbed the WS connection first)
- **openclaw-upgrade-safe.sh**: Replace `openclaw-staging-start/stop` helper script calls with `launchctl kickstart -k ai.openclaw.staging` directly, satisfying `test_openclaw_upgrade_safe_uses_staging_launchagent_not_deleted_helper`
- **exten...

## Key Changes
- 4 commit(s) in this PR
- 4 file(s) changed

- Merged: 2026-04-11

## Commit Messages
1. [Auto] Pending changes committed 2026-04-11 01:14
2. [agento] fix(deploy): disable slack_e2e_matrix in staging+prod monitor; fix upgrade-safe to use launchd label
  
  - deploy.sh: add OPENCLAW_MONITOR_SLACK_E2E_MATRIX_ENABLE=0 for both staging
    and prod monitor runs — DM e2e tests fail when both gateways share the same
    socket-mode app token (Slack routes DMs to whichever grabbed the connection)
  - openclaw-upgrade-safe.sh: replace openclaw-staging-start/stop helper scripts
    with launchctl kickstart -k ai.openclaw.staging directly, as required by
    test_openclaw_upgrade_safe_uses_staging_launchagent_not_deleted_helper
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
3. [agento] fix(mem0-plugin): align degradation log message to test spec
  
  test_mem0_plugin_degrades_invalid_oss_fact_output_to_noop expects
  'degrading add() to a no-op' without 'auto-capture' prefix
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
4. fix: update fatal error log path to staging-gateway.log
  
  CodeRabbit pointed out the fatal error message references gateway.log
  but the staging plist writes to staging-gateway.log.
  
  Fixes coderabbitai review comment on PR #543.

## Files Changed
- `extensions/openclaw-mem0/index.ts`
- `extensions/openclaw-mem0/package.json`
- `scripts/deploy.sh`
- `scripts/openclaw-upgrade-safe.sh`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **1...

2. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 543 --repo jleechanorg/jleechanclaw --json state,merg...

4. @coderabbitai all good?

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 543 --repo jleechanorg/jleechanclaw --json state,merg...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 543 --repo jleechanorg/jleechanclaw --json state,merg...

8. ## Green Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=3 |
| 2. No conflicts | PASS | mergeable=true, state=unstable |
| 3. CR approved | PASS | state=APPROVED...

