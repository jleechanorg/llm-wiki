---
title: "[agento] [P1] fix bug-hunt: agents fail silently → proper error reporting + /tmp output"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-04
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/487
pr_number: 487
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
bug-hunt-daily.sh reported "0 bugs found" as a clean sweep after all 5 bug-hunt agents failed completely (Codex had CA certificate errors, others produced 0-byte output files). Root causes: `|| true` on all agent invocations swallowed failures, empty output files were counted as 0 bugs (not failures), outputs went to ~/.openclaw/bug_reports/ (polluting the live repo), and Codex was invoked with a broken flag.

## Goals
- Agents that fail or produce empty output counted as failures,...

## Key Changes
- 6 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-04

## Commit Messages
1. [fix] bug-hunt: agents fail silently → proper error reporting + /tmp output
2. fix(bug-hunt): count unrecognized-JSON-shape agents as failures; fix heredoc $'\n' newline
3. fix(bug-hunt): exit 1 when all agents fail; include FAILURE_WARNING in report
4. fix(bug-hunt): track agent exit codes in wait loop; distinguish timeout (137) from failure
5. fix(bug-hunt): only count non-zero non-timeout exits as failures (not exit 0)
6. fix(bug-hunt): prevent double-counting AGENT_FAILURES across wait and parse loops

## Files Changed
- `scripts/bug-hunt-daily.sh`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **9...

2. @coderabbitai all good?

3. ## Skeptic Gate Findings

```
VERDICT: PASS

The PR makes several improvements to the bug-hunt script:

1. **Better failure detection**: Added explicit tracking of agent failures (missing files, empty files, invalid JSON, parse errors) rather than silently ignoring them.

2. **Fail-closed behavior**...

4. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` Yes, this looks good! Here's a quick summary of the health checks:

**✅ Logic & Safety**
- The **fail-closed** principle is properly enforced: `[ ! -s "$OU...

5. ## Skeptic Gate Findings

```
VERDICT: PASS

The PR refactors the bug-hunt script with several improvements:
- Better failure detection: tracks missing files, empty outputs, invalid JSON, and parse failures
- Fail-closed behavior: explicitly marks 0 bugs as a failure when all agents crashed
- Remove...

6. @coderabbitai all good?

7. @coderabbitai all good?

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` Yes, still all good! 👍 My previous assessment stands — the fail-closed logic, removal of `|| true` guards, `/tmp` redirection, agent failure tracking, and ...

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Yes, all good! As covered in my earlier response above, the PR is in solid shape:

- ✅ **Fail-closed** logic correctly enforced (`[ ! -s "$OUTPUT_FI...

10. ## Skeptic Gate Findings

```
VERDICT: PASS

The changes in this PR are sound improvements to a bug hunt script:

**Logic is correct:**
- Agent failure tracking (`AGENT_FAILURES`, `ALL_AGENTS_FAILED`) is properly implemented with fail-closed semantics
- Empty file check (`! -s`) correctly identifies...

11. ## Skeptic Gate Findings

```
VERDICT: PASS

The PR makes several improvements to the bug-hunt script:

1. **Output directory change**: Moving bug reports from repo to `/tmp` is a good hygiene change to avoid polluting version control with large agent outputs.

2. **Improved failure tracking**: The ...

12. ## Skeptic Gate Findings

```
VERDICT: PASS

The PR improves error handling and reporting in the bug-hunt-daily script with meaningful changes:

**Strengths:**
- Removes `|| true` from agent invocations so failures are properly detected instead of silently ignored
- Adds comprehensive checks for mis...

13. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR details, CI status, and comments
gh pr view 487 --repo jleechanorg/jleechanclaw ...

15. @coderabbitai all good?

16. @coderabbitai all good?

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` Still all good! ✅ My full automation review just above this comment (at commit `719f4088`) confirmed:

- **10/10 CI checks passing**, clean merge, no confl...

18. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Yes, still all good! ✅ My full automation review at commit `719f4088` stands:

| Category | Status |
|----------|--------|
| **CI Checks** | ✅ 10/10...

19. ## Skeptic Gate Findings

```
VERDICT: PASS

This PR improves the bug-hunt-daily.sh script in several meaningful ways:

1. **Better agent failure tracking**: The new `AGENT_FAILURES` counter properly detects when agents produce no output, empty files, invalid JSON, or unparseable results.

2. **Fail...

20. ## Skeptic Gate Findings

```
VERDICT: PASS

The PR improves the bug-hunt-daily.sh script with several quality improvements:

1. **Enhanced failure detection**: The script now properly tracks agent failures (missing output, empty output, invalid JSON, unparseable counts) instead of silently treating...

21. @coderabbitai all good?

22. @coderabbitai all good?

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Yes, still all good! ✅ As confirmed in my full automation review at commit `719f4088`:

| Category | Status |
|----------|--------|
| **CI Checks** ...

24. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` Still all good! ✅ My full automation review at commit `719f4088` remains current:

| Category | Status |
|----------|--------|
| **CI Checks** | ✅ 10/10 PA...

25. @coderabbitai all good?

26. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Yes, still all good! ✅ My full automation review at commit `719f4088` remains current:

| Category | Status |
|----------|--------|
| **CI Checks** ...

27. @coderabbitai all good?

28. @coderabbitai all good?

29. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Yes, still all good! ✅ My full automation review at commit `719f4088` remains current:

| Category | Status |
|----------|--------|
| **CI Checks** ...

30. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 487 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

31. 🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Evidence Review

**VERDICT: PASS**

**Claim class:** Integration/script — not E2E. The PR is a self-contained cron automation (scripts/bug-hunt-daily.sh). No raw artifact bundle required.

### Verified behaviors (5 criteria)

1. **Ag...

32. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

33. PR is green (7/7 criteria met — awaiting auto-merge)

- CI: Skeptic Gate VERDICT: PASS ✓
- MERGEABLE: true ✓
- CR: APPROVED ✓
- Bugbot: neutral (0 error-severity) ✓
- Inline comments: 15 stale from superseded commits — all addressed ✓
- Evidence review: PASS ✓
- Skeptic: VERDICT: PASS ✓

🤖 Generated...

34. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | FAIL | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=0 (timeout waiting for CI) |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR app...

35. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 487 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

