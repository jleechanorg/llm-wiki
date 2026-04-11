---
title: "[P1] fix(bug-hunt): use openclaw agent one-shot instead of fire-and-forget ao spawn"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-11
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/544
pr_number: 544
pr_repo: jleechanorg/jleechanclaw
---

## Summary
### Background

The daily bug-hunt script was using `ao spawn` plus `ao send --no-wait`, which returned before agents finished. That meant the script could report missing or empty findings while agent work was still running elsewhere. Reviewers also found that the follow-up fix-agent path still used the same fire-and-forget pattern, the jq dedupe expression was malformed, timeout handling depended on invalid process-group assumptions, and later review passes found skip, empty-array, preflight, a...

## Key Changes
- 16 commit(s) in this PR
- 4 file(s) changed

- Merged: 2026-04-11

## Commit Messages
1. fix: replace invalid ao --task usage in bug hunt script
2. fix: align bug-hunt prompt with JSON extraction format
  
  Update TASK_PROMPT to explicitly request markdown-fenced JSON output to match the perl extraction regex on line 148. This prevents silent result loss when agents return bare JSON.
3. fix: address PR comments - agent mapping and JSON extraction
  
  - Add case statement to map AGENT names to openclaw agent handles
  - Add perl extraction to get JSON from markdown code fences
  - Update TASK_PROMPT to request JSON in code fence
  
  Addresses:
  - All five agents hardcoded to same --agent main (cursor)
  - Multiline grep regex never matches (cursor)
  - head -1 truncates multiline JSON (cursor)
  - Prompt and extraction format mismatch (cursor)
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
4. fix: escape backticks and add missing closing quote in bug-hunt-daily.sh
  
  - Escape triple backticks in TASK_PROMPT to prevent command substitution
  - Add missing closing double-quote for TASK_PROMPT variable assignment
5. fix(bug-hunt): process group kill for openclaw tree; loosen JSON fence extraction
6. fix(bug-hunt): remove competing file redirect from subshell (cursor[bot] fix)
7. fix(bug-hunt): move openclaw check before subshell; enable monitor mode for PGID kill
8. fix: use positive PID in kill to properly terminate hung openclaw agents
  
  The timeout watchdog was using 'kill -TERM -PID' (negative PID) to send SIGTERM to a process group, but in a non-interactive bash script without 'set -m', background subshells do not become process group leaders. This caused the kill to fail silently with ESRCH, breaking the timeout safety net. Changed to 'kill -TERM PID' (positive PID) to target the process directly.
9. fix(bug-hunt): setsid for own PGID; --message long flag; pre-check agent subcommand
10. fix(bug-hunt): restore PGID kill after Cursor reverted it (with shopt -s monitor as prerequisite)
11. fix: remove unclosed outer subshell in bug-hunt-daily.sh
  
  The outer subshell opening parenthesis at line 151 was never closed,
  causing a syntax error that prevented the script from running. Removed
  the unnecessary outer subshell since the inner subshell (lines 169-173)
  already handles backgrounding.
12. fix: remove set -m from subshell to enable watchdog process-group kill
  
  Removing set -m from inside the backgrounded subshell allows the openclaw | perl pipeline to inherit the subshell's PGID (already set by parent's shopt -s monitor). This ensures kill -TERM -$PID targets the entire process tree, not just the subshell.
13. fix: complete bug hunt openclaw one-shot dispatch
14. fix: guard empty bug hunt agent wait loop
15. fix: cache bug hunt openclaw preflight
16. fix: align openclaw message flag fallback

## Files Changed
- `.beads/issues.jsonl`
- `scripts/bug-hunt-daily.sh`
- `scripts/thread-reply-nudge.sh`
- `tests/test_bug_hunt_daily_script.py`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: review paused by coderabbit.ai -->

> [!NOTE]
> ## Reviews paused
> 
> It looks like this branch is under active development. To avoid overwhelming you with review comments due to an influx...

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
`@jleechan2015` Let me take a closer look at the changes in this PR and get back to you with a full review!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-...

4. @coderabbitai review

5. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions`[bot] I'll take a thorough look at the PR changes and provide a full review!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already...

8. @coderabbitai all good?

9. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions` I'll do a thorough review of the PR changes right now and get back with a complete assessment!

<details>
<summary>✅ Actions performed</summary>

Full review triggered.

</details>

10. @coderabbitai all good?

11. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me read the script to give you a substantive assessment.

---

🏁 Script executed:
```
#!/bin/bash
fd -i "bug-hunt-daily....

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

14. @coderabbitai all good?

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

16. @coderabbitai all good?

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

18. @coderabbitai review

19. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

20. @coderabbitai all good?

21. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me check the current state of the PR and script before answering.

---

🏁 Script executed:
```
#!/bin/bash
echo "=== PR ...

22. @coderabbitai all good?

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me check the current state of the PR before answering.

---

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="...

24. @coderabbitai all good?

25. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

26. @coderabbitai all good?

27. @coderabbitai all good?

28. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

29. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

30. @coderabbitai all good?

31. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

32. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

33. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

34. @coderabbitai all good?

35. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

36. @coderabbitai all good?

37. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

38. @coderabbitai all good?

39. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

40. @coderabbitai all good?

41. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

42. @coderabbitai all good?

43. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 544 --repo jleechanorg/jleechanclaw --json state,merg...

44. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #544: [P1] fix(bug-hunt): use openclaw agent one-shot instead of fire-and-forget ao spawn — replaces `ao spawn`/`ao send --no-wait` with synchronous `openclaw agent` one-s...

45. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me check the current state of the PR before responding to the skeptic agent's questions.

---

🏁 Script executed:
```
#!...

46. ## Green Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=3 |
| 2. No conflicts | PASS | already merged |
| 3. CR approved | PASS | state=APPROVED |
| 4. Bugbot c...

