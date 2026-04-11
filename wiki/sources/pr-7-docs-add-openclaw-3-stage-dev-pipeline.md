---
title: "docs: add OpenClaw 3-stage dev pipeline"
type: source
tags: [github, pr, jleechanorg-smartclaw]
sources: []
date: 2026-04-02
pr_url: https://github.com/jleechanorg/smartclaw/pull/7
pr_number: 7
pr_repo: jleechanorg/smartclaw
---

## Summary
Adds `docs/openclaw-dev-pipeline.md` — a fully automated 3-stage development pipeline:

**Stage 1 — Feature worktrees + integration tests**
- `~/.openclaw-worktrees/feat-*/` — one worktree per feature
- Python test suite runs without a full gateway
- PR → CodeRabbit review → skeptic-cron merges

**Stage 2 — Staging Docker gateway**
- `~/.openclaw-staging/` as a git worktree on `staging` branch
- Docker container runs the full gateway
- On merge to staging: Docker restarts, integration tests run,...

## Key Changes
- 13 commit(s) in this PR
- 2 file(s) changed

- Merged: 2026-04-02

## Commit Messages
1. docs: add OpenClaw 3-stage dev pipeline (worktrees → Docker staging → prod)
2. Merge main into feat/openclaw-dev-pipeline
3. docs: address CodeRabbit review on 3-stage dev pipeline
  
  - Label ASCII fences (MD040); smartclaw repo naming in diagram
  - Feature worktree checks out feat branch; tests/py snippets use worktree paths
  - os.path.expanduser for openclaw.json validation example
  - ai.openclaw.gateway + kickstart; staging-promote health fail-fast + REPO_SLUG
  - Clarify push vs local hook automation; hooks via git-common-dir for worktrees
  
  Made-with: Cursor
4. docs: add OpenClaw 3-stage dev pipeline (worktrees → Docker staging → prod)
5. docs: address CodeRabbit review on 3-stage dev pipeline
  
  - Label ASCII fences (MD040); smartclaw repo naming in diagram
  - Feature worktree checks out feat branch; tests/py snippets use worktree paths
  - os.path.expanduser for openclaw.json validation example
  - ai.openclaw.gateway + kickstart; staging-promote health fail-fast + REPO_SLUG
  - Clarify push vs local hook automation; hooks via git-common-dir for worktrees
  
  Made-with: Cursor
6. docs: fix setup order, prod worktree, unified post-commit hook
  
  - Create origin/staging before staging worktree add; document detached prod option
  - Single post-commit with path dispatch; canonical ~/.openclaw/scripts/staging-promote.sh
  
  Made-with: Cursor
7. Merge remote-tracking branch 'origin/feat/openclaw-dev-pipeline' into feat/openclaw-dev-pipeline
  
  Made-with: Cursor
8. docs: address PR review threads (hooks, health curl, staging doc link)
  
  - Link to openclaw-staging-setup.md; document git-path/common-dir for linked worktrees
  - post-merge copy for ff-only pulls; curl || true under set -e in staging-promote
  - Optional TOKEN_FILE -> STAGING_GATEWAY_TOKEN; clarify Python expanduser comment
  
  Made-with: Cursor
9. Merge main into feat/openclaw-dev-pipeline
10. docs: link Docker staging guide after merge from main
  
  Made-with: Cursor
11. docs: create staging branch from origin/main in setup
  
  Made-with: Cursor
12. docs: tighten gh pr create error handling; single hook script reference
  
  - On gh pr create failure, only skip if a staging→main PR already exists
  - Remove duplicated post-commit block from Getting Started; link to Automation section
  
  Made-with: Cursor
13. chore: ignore .gateway-token; document staging token safety
  
  Made-with: Cursor

## Files Changed
- `.gitignore`
- `docs/openclaw-dev-pipeline.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: review paused by coderabbit.ai -->

> [!NOTE]
> ## Reviews paused
> 
> It looks like this branch is under active development. To avoid overwhelming you with review comments due to an influx...

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
# Get PR details, status, and comments
gh pr view 7 --repo jleechanorg/smartclaw --json t...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #7: docs: add OpenClaw 3-stage dev pipeline — claims to add a complete automated feature→staging→production promotion process in `/Users/jleechan/repos/smartclaw/docs/open...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Yes, I **agree with the Skeptic Agent's FAIL verdict**. The analysis is consistent with my own findings from the earlier review chain.

Here is my confir...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] — **Not yet.** The PR remains in `CHANGES_REQUESTED` state with the following blockers still unresolved:

| Priority | Issue |
|----------|-------|
...

8. @coderabbitai all good?

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,merge...

10. @coderabbitai all good?

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,merge...

12. @coderabbitai Addressed the follow-up: staging-before-worktree ordering, prod worktree + detached fallback, canonical `~/.openclaw/scripts/staging-promote.sh`, and a single path-based `post-commit` (no duplicate hook writes).

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,merge...

14. @coderabbitai all good?

15. @coderabbitai all good?

16. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,merge...

18. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,mergeable,mergeStateStatus,r...

19. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,merge...

20. @coderabbitai all good?

21. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,mergeable,mergeStateStatus,r...

22. @coderabbitai all good?

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,mergeable,mergeStateStatus,r...

24. @coderabbitai Staging setup now uses `git checkout -B staging origin/main` (commit 3340c8a+). All review threads are resolved. Please post an APPROVED review if the doc looks good.

25. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,mergeable,mergeStateStatus,r...

26. @coderabbitai all good?

27. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,mergeable,mergeStateStatus,r...

28. @coderabbitai all good?

**Status check:** Head `9991872` — `cd "$STAGING_DIR"` for pytest, curl `|| true` + `GATEWAY_HEALTHY`, `gh pr create` failure handling (no blanket `|| echo`), single hook reference + `.gateway-token` in `.gitignore`. All 31 review threads resolved; Cursor Bugbot + CodeRabbit...

29. **Merged** via API (squash) — merge commit `568ef0f`. Local `gh pr merge` hit a worktree checkout conflict; REST merge succeeded.

30. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 7 --repo jleechanorg/smartclaw --json title,state,mergeable,mergeStateStatus,r...

