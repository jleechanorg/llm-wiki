---
title: "[agento] fix(launchd): remove duplicate com.openclaw.gateway plist template"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-05
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/511
pr_number: 511
pr_repo: jleechanorg/jleechanclaw
---

## Summary
### Background
Root cause of recurring gateway orphan processes: `launchd/` directory has BOTH `ai.openclaw.gateway.plist` (canonical) AND `com.openclaw.gateway.plist` (legacy). `install-launchagents.sh` installs both during deploy Stage 3.5, creating two competing gateway instances on the same port/state-dir → lock storms → WS pong starvation.

### Goals
Eliminate the source of duplicate gateway plists so deploys never create competing instances.

### Changes
1. Delete `launchd/com.openclaw.gat...

## Key Changes
- 6 commit(s) in this PR
- 5 file(s) changed

- Merged: 2026-04-05

## Commit Messages
1. [agento] fix(launchd): remove duplicate com.openclaw.gateway plist template
  
  Root cause of recurring gateway orphan processes: launchd/ directory has BOTH
  ai.openclaw.gateway.plist (canonical) and com.openclaw.gateway.plist (legacy).
  install-launchagents.sh installs both during deploy Stage 3.5, creating two
  competing gateway instances on the same port/state-dir.
  
  Removing the legacy template. gateway-preflight.sh --fix already cleans up
  installed copies, but the source template in launchd/ kept recreating it.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
2. [agento] fix(deploy): remove legacy com.openclaw.gateway fallback from Stage 4
  
  deploy.sh tried com.openclaw.gateway first, then ai.openclaw.gateway as fallback.
  Since the legacy plist template is now deleted, simplify to only ai.openclaw.gateway.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
3. [agento] fix(install): use ai.openclaw.gateway as canonical label, remove legacy com.openclaw.gateway
  
  install-launchagents.sh was installing com.openclaw.gateway and tearing down
  ai.openclaw.gateway — exactly backwards. This caused the gateway to flip between
  labels on each deploy, and preflight.sh --fix would re-add the 'correct' one,
  resulting in two competing gateway instances.
  
  Fixes:
  - Install ai.openclaw.gateway.plist (canonical)
  - Tear down legacy com.openclaw.gateway on successful install
  - Update EXPECTED_LABELS verification to use ai.openclaw.gateway
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
4. [agento] fix(deploy): add fail-fast label assertions after gateway restart
  
  CR feedback: port-based single-instance check doesn't guarantee the canonical
  ai.openclaw.gateway label is loaded (vs legacy com.openclaw.gateway). Add
  explicit launchctl list assertions after restart to fail-fast if labels are wrong.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. fix(staging-canary): use ai.openclaw.gateway label to find Node binary
6. [agento] fix(plist): add OPENCLAW_STATE_DIR + fix log paths to use prod dir
  
  Prod gateway plist was missing OPENCLAW_STATE_DIR and OPENCLAW_CONFIG_PATH,
  causing it to default to ~/.openclaw/ (staging dir). This meant:
  - Prod and staging shared session lock files (lock storms)
  - Prod logs went to staging log dir (confusing diagnostics)
  - CLAUDE.md said prod uses ~/.openclaw_prod but the plist didn't enforce it
  
  Adds OPENCLAW_STATE_DIR=/Users/jleechan/.openclaw_prod and
  OPENCLAW_CONFIG_PATH to EnvironmentVariables. Fixes StandardErrorPath
  and StandardOutPath to use ~/.openclaw_prod/logs/.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `launchd/ai.openclaw.gateway.plist`
- `launchd/com.openclaw.gateway.plist`
- `scripts/deploy.sh`
- `scripts/install-launchagents.sh`
- `scripts/staging-canary.sh`

## Review Notes
1. @coderabbitai all good?

2. @coderabbitai review

3. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **1...

4. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

5. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions`[bot] I'll perform a fresh review of the PR to confirm everything looks good!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review alread...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] — yes, the changes look good overall! Here's a quick summary of what was reviewed:

**✅ What the PR does correctly:**
- Removes the legacy `launchd/...

8. ## Hourly Monitor Cycle — 2026-04-05T17:18 UTC

- Open PRs: 1 (#511)
- 7-green merges: 0
- Stuck PRs (>48h): none (PR #511 is ~4 minutes old)
- CI failures: none on main
- Issues created: none

### PR #511 — age: 0h 4m — status: concerning

**7-green gate status** (per Skeptic Gate + live check):

|...

9. @coderabbitai all good?

10. @coderabbitai all good?

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Not quite yet! Based on the monitor cycle you posted, there are still a few open items blocking the 7-green gate:

**Failing/Warning Gates:**
| Gate | St...

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Not quite yet! Based on the gate status your monitor reported and my earlier review, there are a few items still open before this is merge-ready:

---

*...

13. @coderabbitai approve

The fail-fast label assertions requested in the review have been added in commit d1fbe0f. After gateway restart, deploy.sh now:
1. Asserts `ai.openclaw.gateway` is loaded (`launchctl list` must succeed)
2. Asserts `com.openclaw.gateway` is NOT loaded (`launchctl list` must fai...

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Thanks for the update! The fail-fast assertions you've described in commit `d1fbe0f` directly address my blocking concern:

- ✅ Assert `ai.openclaw.gatew...

15. @coderabbitai all good?

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — From **CodeRabbit's side, yes — all good!** ✅ The PR is approved.

Here's the current gate status from my perspective:

| Gate | Status |
|------|-------...

17. @coderabbitai all good?

18. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] — From **CodeRabbit's side, yes — all good!** ✅ The PR is approved.

| Gate | Status |
|------|--------|
| Duplicate plist removed | ✅ |
| `deploy.s...

19. @coderabbitai all good?

20. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions` — From **CodeRabbit's side, yes — all good!** ✅ The PR is approved.

| Gate | Status |
|------|--------|
| Duplicate plist removed | ✅ |
| `deploy.sh` St...

21. @coderabbitai approve

22. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Comments resolved and changes approved.

</details>

23. @coderabbitai review

24. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

25. ## PR is green (7/7 criteria met — awaiting auto-merge)

| # | Condition | Status |
|---|-----------|--------|
| 1 | CI green | PASS — Skeptic Gate + Staging Canary + find-openclaw-json + ping-coderabbit ✓ |
| 2 | No conflicts | PASS — mergeable=true |
| 3 | CR APPROVED | PASS — coderabbitai APPROVE...

26. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

27. PR is green (7/7 criteria met — awaiting auto-merge)

| # | Gate | Result |
|---|------|--------|
| 1 | CI passing | PASS |
| 2 | No conflicts | PASS |
| 3 | CR APPROVED | PASS (2026-04-05T17:34:40Z) |
| 4 | Bugbot clean | PASS |
| 5 | Threads resolved | PASS |
| 6 | Evidence | N/A (config/deploy fi...

