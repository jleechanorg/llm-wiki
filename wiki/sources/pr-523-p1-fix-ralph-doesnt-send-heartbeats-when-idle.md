---
title: "[P1] fix: ralph doesn't send heartbeats when idle"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-06
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/523
pr_number: 523
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
Ralph sessions were being flagged as stuck or killed by the orchestrator because they weren't responding to heartbeat polls. This happened because ralph runs agents (like Claude Code) by piping input, which prevents the agent from seeing interactive heartbeat polls typed into the tmux pane.

## Goals
Ensure ralph always responds to orchestrator heartbeat polls, even when the agent is busy or between iterations.

## Tenets
- Robustness: Use background loops to monitor for polls.
- N...

## Key Changes
- 5 commit(s) in this PR
- 3 file(s) changed

- Merged: 2026-04-06

## Commit Messages
1. fix: [P1] ralph doesn't send heartbeats when idle
2. fix(ralph): consolidate heartbeat logic and prevent double-ack
  
  - Use _respond_to_heartbeat helper from terminal_recorder.sh in both loops.
  - Improve detection to scan full captured content and compare line numbers.
  - Use capture-pane -S -50 for efficiency.
  - Add mkdir-based sentinel lock to prevent simultaneous heartbeat responses.
  - Remove stdin-polluting send-keys fallback.
  - Add test cases for heartbeat detection and response.
3. fix(ralph): harden heartbeat logic and tests
  
  - Add staleness check for heartbeat sentinel (Linux+macOS compatible).
  - Add warning log when pane TTY is not writable.
  - Protect heartbeat write and helper calls with || true to avoid set -e termination.
  - Fix test flakiness with explicit sentinel cleanup and wait between scenarios.
4. fix(ralph): address final review comments on heartbeat logic
  
  - Use exact line matching (grep -nFx) for protocol markers.
  - Fix grep -c corruption in tests.
  - Update EXIT trap to include test-heartbeat session.
  - Improve test reliability with explicit cleanup and better counts.
5. fix(ralph): avoid exact line match for heartbeat and obfuscate literals
  
  - Remove -x from grep to allow matching heartbeat prompts with extra context.
  - Obfuscate protocol strings in the script to prevent it from matching its own source code when printed.

## Files Changed
- `ralph.sh`
- `ralph/lib/terminal_recorder.sh`
- `ralph/tests/test_terminal_recorder.sh`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **8...

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
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,merg...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec -
OpenAI Codex v0.117.0 (research preview)
--------
workdir: /Users/jleechan/.openclaw
model: gpt-5.3-code...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — responding to the Skeptic Agent's consultation (`@coderabbitai — agree with this analysis?`):

**Yes, I agree with the FAIL verdict.** The infrastructure...

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
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,merg...

8. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

9. @coderabbitai all good

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,merg...

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,merg...

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
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,merg...

14. @coderabbitai all good (sentinel staleness + TTY write failure + test flakiness fixed)

15. <!-- This is an auto-generated reply by CodeRabbit -->
`@jleechan2015` — thanks for the confirmation! I'll kick off a fresh review of the latest commit to verify the sentinel staleness fix, TTY write failure handling, and test flakiness resolutions, and update my `CHANGES_REQUESTED` gate accordingly...

16. @coderabbitai all good?

17. @coderabbitai all good (exact line match + test cleanup + grep corruption fixed)

18. <!-- This is an auto-generated reply by CodeRabbit -->
`@jleechan2015` — thanks for the update! I'll trigger a fresh incremental review to verify the exact line match logic, test cleanup, and grep corruption fixes, and clear my `CHANGES_REQUESTED` gate if everything checks out.

<!-- <review_comment...

19. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,isDraft,reviewDecision,title,headRefOid 2>&1

echo ...

20. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

21. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,merg...

22. @coderabbitai all good?

23. @coderabbitai all good (exact line match removed + obfuscated literals)

24. <!-- This is an auto-generated reply by CodeRabbit -->
`@jleechan2015` — thanks for confirming! I'll trigger a fresh incremental review to verify that the exact-line match logic has been removed and that the protocol marker literals are now obfuscated to prevent self-triggering.

<!-- <review_commen...

25. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,merg...

26. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

27. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

28. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 523 --repo jleechanorg/jleechanclaw --json state,merg...

