---
title: "fix(deploy): protect staging gateway during prod restart + increase startup wait"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-05
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/507
pr_number: 507
pr_repo: jleechanorg/jleechanclaw
---

## Summary
### Background

Deploy has been failing repeatedly because the orphan-kill step in Stage 4 kills the **staging** gateway (port 18810) along with prod orphans. This triggers a launchd KeepAlive restart loop on staging, which appears dead during the monitor-agent health check — causing a 5+ minute hang and deploy failure.

### Root Cause

 in Stage 4 indiscriminately kills ALL gateway processes, including the staging gateway. Since staging's KeepAlive immediately respawns it, the orphan check sees...

## Key Changes
- 5 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-05

## Commit Messages
1. fix(deploy): protect staging gateway during prod restart + increase startup wait
2. fix(deploy): handle edge cases in staging-gateway protection
  
  - Guard grep -vFxf with empty _staging_pids (no exclusion when staging is down)
  - Log which port each killed orphan was on (diagnostic aid)
  - Fix comment: reference STAGING_PORT variable, not hardcoded 18810
3. fix(deploy): add || true to lsof pipeline under pipefail
4. fix(deploy): guard lsof exit with || true outside subshell, fix orphan kill loop
  
  Bugbot P1: lsof | sort -u || true placed || inside the substitution,
  so only sort exit was guarded. Fix: move || true outside the $().
  
  Also fix the orphan-kill loop: xargs had undefined port variable, wrong
  lsof syntax, and && chain that skipped kill on echo failure. Replace
  with while-read loop using lsof -i -P -n -a -p "$pid" for per-PID
  port lookup, kills each orphan independently.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. fix(deploy): guard pgrep/lsof against pipefail exit 1

## Files Changed
- `scripts/deploy.sh`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **2...

2. @coderabbitai review

3. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

4. @coderabbitai review

5. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

6. @coderabbitai all good?

7. @coderabbitai review

8. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

9. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions` I'll run a fresh review to check the current state of the PR!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed comm...

10. @coderabbitai all good?

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get the diff for PR `#507`
gh pr diff 507 --repo jleechanorg/jleechanclaw
```

Length o...

12. @coderabbitai all good?

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] — **Almost, but not quite yet.** Here's the current status:

### ✅ Functionally correct
- Staging-PID exclusion via `lsof` on port 18810 — works cor...

14. @coderabbitai review

15. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

16. ## Evidence Review

**Claim**: pipeline E2E (CI/CD deploy script change)
**Verdict**: PASS

**Evidence**:
- CI checks (head commit ec8798f13): Staging Canary Gate: success (x4), all other check runs passing
  - https://github.com/jleechanorg/jleechanclaw/actions/runs/23998436474
  - https://github.c...

17. PR is green (7/7 criteria met — awaiting auto-merge)

| # | Condition | Status |
|---|-----------|--------|
| 1 | CI green | PASS — Staging Canary Gate ✓, Skeptic Gate ✓ |
| 2 | No conflicts | PASS — mergeable=clean |
| 3 | CR APPROVED | PASS — coderabbitai[bot] APPROVED |
| 4 | Bugbot clean | PASS ...

18. PR #507 is green (7/7 criteria met — awaiting auto-merge)

19. @coderabbitai review

20. @coderabbitai all good?

21. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

22. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr diff 507 --repo jleechanorg/jleechanclaw
```

Length of output: 4006

---



</deta...

23. EVIDENCE BUNDLE REVIEW: INSUFFICIENT
PR: https://github.com/jleechanorg/jleechanclaw/pull/507
Current HEAD: 1f5018ad8754b8f2ceb4da6ce478bea2007b9114

Claim class: Pipeline E2E

---

VERDICT: INSUFFICIENT

Evidence claimed vs. actual:

| Claimed | Actual |
|---|---|
| Commit f985105698 contains both ...

24. @coderabbitai all good?

25. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get latest diff
gh pr diff 507 --repo jleechanorg/jleechanclaw

echo "=== PR STATUS ===...

26. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | already merged |\n| 3. CR approved | PASS | state=APPROVED |\n| 4. Bug...

27. PR is green (7/7 criteria met — awaiting auto-merge)

