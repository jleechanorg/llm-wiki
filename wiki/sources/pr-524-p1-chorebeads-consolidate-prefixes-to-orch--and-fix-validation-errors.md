---
title: "[P1] chore(beads): consolidate prefixes to orch-* and fix validation errors"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-06
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/524
pr_number: 524
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
The beads tracker had a mix of `jleechan-*` and `orch-*` prefixes in `.beads/issues.jsonl`, causing `br list` to error out during prefix validation when `issue-prefix` was set to `jleechan`.

## Goals
- Consolidate all beads IDs to use the `orch-*` prefix consistently.
- Fix schema validation errors in `issues.jsonl`.
- Unblock `br` CLI usage for all agents.

## Tenets
- Consistency: Use a single prefix for all issues.
- Validity: Ensure all JSONL entries pass `br` validation check...

## Key Changes
- 3 commit(s) in this PR
- 4 file(s) changed

- Merged: 2026-04-06

## Commit Messages
1. chore(beads): consolidate prefixes to orch-* and fix validation errors
2. docs(roadmap): fix inconsistencies after prefix consolidation and robustify guidance_tracker regex
3. fix(beads): restore original description for orch-f7l to describe previous mismatch

## Files Changed
- `.beads/config.yaml`
- `.beads/issues.jsonl`
- `roadmap/README.md`
- `src/orchestration/guidance_tracker.py`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **0...

2. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
Based on my analysis:

**Evidence Review (Rule 10)**: The PR description contains testing statements:
- "Verified `br list` works without errors."
- "Verified `br show orch-f7l` works and ...

3. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

4. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 524 --repo jleechanorg/jleechanclaw --json state,merg...

5. @coderabbitai all good?

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 524 --repo jleechanorg/jleechanclaw --json state,merg...

7. @coderabbitai all good? I have fixed the inconsistencies in roadmap/README.md and made the regex in guidance_tracker.py more robust as requested.

8. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Neither Codex nor Claude CLI available for skeptic evaluation

_Posted by jleechan2015 · 2026-04-06T10:20:30.991Z_
<!-- skeptic-gate-trigger-2f2e931adeb5c19d1e8ce54c...

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 524 --repo jleechanorg/jleechanclaw --json state,merg...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 524 --repo jleechanorg/jleechanclaw --json state,merg...

11. @coderabbitai all good?

12. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 524 --repo jleechanorg/jleechanclaw --json state,merg...

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 524 --repo jleechanorg/jleechanclaw --json state,merg...

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 524 --repo jleechanorg/jleechanclaw --json state,merg...

16. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | already merged |\n| 3. CR approved | PASS | state=APPROVED |\n| 4. Bug...

