---
title: "[P1] fix(hooks/mem0_config): handle unexpanded env vars as empty strings"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-06
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/528
pr_number: 528
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
A recent merge of PR #520 introduced a regression (flagged by Cursor Bugbot) where unexpanded environment variables in `openclaw.json` (e.g., `"apiKey": "$OPENAI_API_KEY"`) were treated as literal strings when the variable was unset. This caused `mem0_hooks_enabled()` to return `True`, leading to failed API calls rather than failing open.

## Goals
- Correctly handle unexpanded environment variables by treating them as empty strings.
- Prevent hooks from attempting API calls with i...

## Key Changes
- 3 commit(s) in this PR
- 2 file(s) changed

- Merged: 2026-04-06

## Commit Messages
1. fix(hooks/mem0_config): handle unexpanded env vars as empty strings
2. fix(hooks/mem0_config): expand regex to handle lowercase env vars
3. fix: type guard in hooks and align shared client env expansion

## Files Changed
- `.claude/hooks/mem0_config.py`
- `scripts/mem0_shared_client.py`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- walkthrough_start -->

<details>
<summary>📝 Walkthrough</summary>

## Walkthrough

A helper to safely expand environment variables was added and used to replace direct `os.path.expandvars` calls when normalizing embedder and...

2. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
Looking at this PR's status, I can identify several concrete gaps:

## Background
PR #528: Fix handling of unexpanded env vars in mem0_config.py — claims to fix a regression where unset en...

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Responding to the Skeptic Agent's `@coderabbitai` consultation:

**Important context first:** The Skeptic Agent's FAIL verdict was itself an **infrastruc...

4. @coderabbitai all good?

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status including reviews, CI checks, and comments
gh pr view 528 --repo ...

6. @coderabbitai all good

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Thanks for confirming! To make sure we're aligned: when you say "all good," did you push the regex broadening fix (adding `a-z` to the character class)?
...

8. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec -
OpenAI Codex v0.117.0 (research preview)
--------
workdir: /Users/jleechan/.openclaw
model: gpt-5.3-code...

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state: reviews, CI, and unresolved comments
gh pr view 528 --repo jlee...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state: reviews, CI, and review threads
gh pr view 528 --repo jleechano...

11. @coderabbitai all good?

12. @coderabbitai all good

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state
gh pr view 528 --repo jleechanorg/jleechanclaw --json state,revi...

14. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec -
OpenAI Codex v0.117.0 (research preview)
--------
workdir: /Users/jleechan/.openclaw
model: gpt-5.3-code...

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state, reviews, CI, and review threads
gh pr view 528 --repo jleechano...

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state, reviews, CI, and review threads
gh pr view 528 --repo jleechano...

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
# Get current PR state, reviews, CI, and review decision
gh pr view 528 --repo jleechanor...

19. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

