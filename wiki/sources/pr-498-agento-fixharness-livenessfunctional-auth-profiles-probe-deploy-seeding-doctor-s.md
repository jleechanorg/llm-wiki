---
title: "[agento] fix(harness): liveness≠functional — auth-profiles probe, deploy seeding, doctor STATE_DIR check"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-05
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/498
pr_number: 498
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
Silent Slack failure (2026-04-04): OpenClaw bot stopped responding to Jeffrey's messages. Root cause: `auth-profiles.json` was missing from `~/.openclaw_prod/agents/main/agent/` (the prod state dir). HTTP `/health` returned `{"ok":true,"status":"live"}` throughout — every diagnostic check looked green while every LLM call silently failed with "No API key found for provider anthropic".

The plist had also been using `~/.openclaw-production/` (wrong dir) instead of `~/.openclaw_prod/...

## Key Changes
- 5 commit(s) in this PR
- 7 file(s) changed

- Merged: 2026-04-05

## Commit Messages
1. fix(harness): liveness≠functional — auth-profiles probe, deploy seeding, doctor STATE_DIR check
  
  Root cause of 2026-04-04 silent Slack failure: HTTP /health returns live even
  when auth-profiles.json is missing from OPENCLAW_STATE_DIR. Every LLM call fails
  silently with 'No API key found for provider anthropic' while gateway appears healthy.
  
  Fixes (orch-zmw, orch-3fz, orch-65m, orch-rp8):
  - staging-canary.sh: Add check 8 -- auth-profiles.json present in state dir (7->8 checks)
  - deploy.sh Stage 3: Seed auth-profiles.json into prod if missing; fail-close if both missing
  - doctor.sh: Add plist OPENCLAW_STATE_DIR consistency check (must match ~/.openclaw_prod/)
    and auth-profiles.json existence check for the plist's configured state dir
  - CLAUDE.md: Document liveness!=functional rule with explicit guidance
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
2. fix(doctor): update GATEWAY_LABEL to com.openclaw.gateway after plist migration
  
  ai.openclaw.gateway plist was replaced by com.openclaw.gateway via
  install-launchagents.sh. doctor.sh GATEWAY_LABEL was not updated,
  causing all plist checks to fail with 'file does not exist'.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
3. chore: refresh docs context snapshot (auto-audit)
4. fix(canary,doctor): harden STATE_DIR checks per CR feedback
  
  - doctor.sh: warn→fail for missing plist OPENCLAW_STATE_DIR (fail-closed);
    auth-profiles check now always runs using expected_state_dir fallback
    so it cannot be skipped when plist_state_dir is unset
  - staging-canary.sh: define PROD_PORT=${OPENCLAW_PROD_PORT:-18789} once
    at top of script; checks 7+8 use PROD_PORT instead of hardcoded 18789
    so custom deployments using OPENCLAW_PROD_PORT resolve correct state dir
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. chore: refresh cron backup

## Files Changed
- `CLAUDE.md`
- `docs/context/CRON_JOBS_BACKUP.md`
- `docs/context/DOC_GAPS.md`
- `docs/context/SYSTEM_SNAPSHOT.md`
- `scripts/deploy.sh`
- `scripts/doctor.sh`
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
`@github-actions` I'll kick off a full review of PR `#498` right away to verify everything looks good — checking the canary check 8 logic, deploy seeding safety, doctor plist parsing robustness, and the CLAUDE.md documentation update.

<details>...

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
set -euo pipefail

REPO="jleechanorg/jleechanclaw"
PR=498

echo "=== PR STATUS ==="
gh pr...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions` Not yet — based on my review at commit `e9d39c6e`, the PR still has **8 unresolved threads** and the merge gate is blocked (`UNSTABLE` / `CHANGES_REQUEST...

8. @coderabbitai all good?

9. @coderabbitai approve

Both findings addressed:
- doctor.sh: warn→fail for missing OPENCLAW_STATE_DIR; auth-profiles check now always runs via expected_state_dir fallback
- staging-canary.sh: PROD_PORT=${OPENCLAW_PROD_PORT:-18789} defined at top; checks 7+8 use it instead of hardcoded 18789

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/jleechanclaw"
PR=498

echo "=== PR STATUS ==="
gh pr...

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me verify the claimed fixes in the code before approving.

---

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

ec...

12. @coderabbitai all good?

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/jleechanclaw"
PR=498

echo "=== LATEST COMMIT ==="
g...

14. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

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
set -euo pipefail

REPO="jleechanorg/jleechanclaw"
PR=498

echo "=== LATEST COMMIT ==="
g...

