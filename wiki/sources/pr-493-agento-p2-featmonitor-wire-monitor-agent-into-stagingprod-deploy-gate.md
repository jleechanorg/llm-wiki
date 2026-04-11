---
title: "[agento] [P2] feat(monitor): wire monitor-agent into staging→prod deploy gate"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-04
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/493
pr_number: 493
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
Jeffrey requested that the staging→prod deploy gate run monitor-agent before pushing to prod, block on failure, and alert both Slack (#all-jleechan-ai C09GRLXF9GR) and email.

## Goals
1. Run monitor-agent BEFORE pushing to prod — BLOCK push if monitor fails
2. Alert Slack (#all-jleechan-ai) AND email with failure details + recommendations
3. Hourly monitor execution via launchd (already exists)
4. Part of bootstrap.sh install (already wired via install-openclaw-launchd.sh)

## Ten...

## Key Changes
- 4 commit(s) in this PR
- 2 file(s) changed

- Merged: 2026-04-04

## Commit Messages
1. feat(monitor): wire monitor-agent into staging→prod deploy gate
  
  - Change FAILURE_SLACK_TARGET default from C0AKYEY48GM → C09GRLXF9GR
    (#all-jleechan-ai) so the whole team sees failures
  - Add email alerting (via send-alert-email.sh) in monitor-agent.sh
    when STATUS=PROBLEM — fires BEFORE Slack exit so email always runs
    as backup even if Slack delivery fails
  - Update deploy.sh die() Slack target to C09GRLXF9GR for consistency
  
  Existing infrastructure already satisfied the other requirements:
  - deploy.sh already calls monitor-agent before staging push (Stage 1)
  - deploy.sh already BLOCKS on monitor failure via || die
  - ai.openclaw.monitor-agent.plist already provides hourly execution
  - install-openclaw-launchd.sh already installed by bootstrap.sh
  
  Closes #6uf
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
2. fix(monitor): add 30s timeout around email send to prevent monitor stalls
  
  Wrap send-alert-email.sh in timeout(1) so a hanging email send does not
  stall the entire monitor-agent run. Per CR feedback, || true handles
  failures but not hangs. Also document the $HOME/.openclaw path assumption.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
3. chore: trigger skeptic gate re-run after CR re-approval
4. fix(monitor): replace GNU timeout with shell-native subshell+sleep kill
  
  Use subshell+sleep+kill timeout instead of GNU timeout(1) so the email
  alert never hangs the monitor even if timeout is unavailable on the PATH.
  The previous GNU timeout approach required coreutils which is not on plain macOS.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `monitor-agent.sh`
- `scripts/deploy.sh`

## Review Notes
1. @coderabbitai all good?

2. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

3. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **1...

4. @coderabbitai all good?

5. @coderabbitai all good?

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Gather PR status, CI checks, merge status, and comments
echo "=== PR STATUS ==="
gh pr ...

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR details, CI status, and comments
gh pr view 493 --repo jleechanorg/jleechanclaw ...

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

9. @coderabbitai review

10. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

11. @coderabbitai all good?

12. @coderabbitai all good?

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

15. @## Evidence Review — Verdict: PASS (with WARN)

**Reviewer**: evidence-reviewer (independent audit, Sonnet 4.6)
**Evidence claim class**: PR-lifecycle E2E (config/script change)
**Focus**: PR description accuracy + implementation correctness

---

### Phase 1 — PR Status (external evidence)

| Gate...

16. @coderabbitai all good?

17. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

18. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

19. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

20. @coderabbitai all good?

21. @coderabbitai all good?

22. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

24. @coderabbitai resume

25. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Reviews resumed.

</details>

26. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

27. @coderabbitai approve

28. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Comments resolved and changes approved.

</details>

29. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

30. @coderabbitai all good?

31. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

32. @coderabbitai all good?

33. @coderabbitai all good?

34. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

35. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

36. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

37. PR is green (7/7 criteria met — awaiting auto-merge)

38. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

39. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 493 --repo jleechanorg/jleechanclaw --json state,merg...

