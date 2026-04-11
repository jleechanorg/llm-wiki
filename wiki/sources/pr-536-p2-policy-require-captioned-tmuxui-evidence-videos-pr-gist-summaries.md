---
title: "[P2] Policy: require captioned tmux/UI evidence videos + PR gist summaries"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-09
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/536
pr_number: 536
pr_repo: jleechanorg/jleechanclaw
---

## Summary
### Background
Evidence standards were partially defined but did not consistently require captioned videos, GitHub-native attachment URLs, sanitized output paths, or PR-level test/gist summaries. This made evidence review inconsistent across agents.

### Goals
1. Require captioned video evidence for terminal and browser claims.
2. Make browser UI video mandatory for user-facing changes.
3. Require GitHub native PR video attachments and standardized PR evidence summary fields.
4. Prevent machine-...

## Key Changes
- 3 commit(s) in this PR
- 2 file(s) changed

- Merged: 2026-04-09

## Commit Messages
1. docs: require captioned tmux and UI evidence videos
2. docs: address policy review feedback for PR 536
3. fix: address CodeRabbit review comments on evidence policy
  
  - Add bootstrapping exemption for policy-definition PRs in CLAUDE.md
  - Strengthen sensitive-data prohibition with "never even if sanitized" clause
  - Clarify browser/UI video is mandatory for user-facing changes
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

## Files Changed
- `CLAUDE.md`
- `workspace/AGENTS.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- walkthrough_start -->

<details>
<summary>📝 Walkthrough</summary>

## Walkthrough

Two repository docs were updated to add a new Evidence Media Policy: mandatory terminal (tmux) videos for non-trivial changes, mandatory brow...

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
# Get PR status, checks, and review comments
gh pr view 536 --repo jleechanorg/jleechancl...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec -
OpenAI Codex v0.117.0 (research preview)
--------
workdir: /Users/jleechan/project_jleechanclaw/jleechan...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, checks, merge conflicts, and review comments
gh pr view 536 --repo jleec...

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state and review details
gh pr view 536 --repo jleechanorg/jleechanclaw ...

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

8. @coderabbitai all good?

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

10. @coderabbitai all good?

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

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
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

14. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #536: [P2] Policy: require captioned tmux/UI evidence videos + PR gist summaries — the PR claims to tighten repo evidence policy by requiring captioned terminal/browser vi...

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

17. @coderabbitai all good?

18. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

19. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

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
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 536 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

24. **VERDICT: PASS** — skeptic-cron evaluated and merged this PR. All 6 criteria confirmed green.  \n\n<!-- HEAD-SHA: a390b9960560b2afaad4cc37ef6cc576c13e75bd -->

