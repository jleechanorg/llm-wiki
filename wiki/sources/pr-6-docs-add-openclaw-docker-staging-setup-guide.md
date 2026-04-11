---
title: "docs: add OpenClaw Docker staging setup guide"
type: source
tags: [github, pr, jleechanorg-smartclaw]
sources: []
date: 2026-04-02
pr_url: https://github.com/jleechanorg/smartclaw/pull/6
pr_number: 6
pr_repo: jleechanorg/smartclaw
---

## Summary
Adds `docs/openclaw-docker-staging-setup.md` as a sibling to `openclaw-staging-setup.md`.

Covers:
- Docker-based staging gateway vs native launchd
- docker-compose configuration with staging credentials  
- Loopback-only port binding (127.0.0.1:18810 → container :18789)
- Control UI origin patching for non-loopback bind
- Start/stop/manage/update/teardown commands

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk documentation-only change; no runtime code or configuration defaul...

## Key Changes
- 4 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-02

## Commit Messages
1. docs: add OpenClaw Docker staging setup guide
2. docs: address CodeRabbit review on Docker staging guide
  
  - Use ${HOME} for compose volume paths; expanduser in Python patch
  - Document security risk of dangerouslyAllowHostHeaderOriginFallback
  - Add language tag to expected-output fenced block
  - Use compose pull + up -d after image updates (not restart)
  
  Made-with: Cursor
3. docs: resolve Copilot/Codex feedback on Docker staging guide
  
  - Use launchctl stop (not bootout) so teardown start works; document bootstrap path
  - Fix GHCR auth: read:packages scope, not read:user alone
  - Single compose volume mount (drop redundant nested workspace bind)
  - Split Control UI patch: allowedOrigins first; optional dangerously* only when needed
  - Recreate containers with up -d --force-recreate after image pull
  
  Made-with: Cursor
4. docs: pin compose project name in Docker staging guide
  
  Aligns container names with verify/troubleshooting examples regardless of working directory.
  
  Made-with: Cursor

## Files Changed
- `docs/openclaw-docker-staging-setup.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: failure by coderabbit.ai -->

> [!CAUTION]
> ## Review failed
> 
> The pull request is closed.

<!-- end of auto-generated comment: failure by coderabbit.ai -->

<details>
<summary>ℹ️ Recen...

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
# Get PR details, comments, reviews, and CI status
gh pr view 6 --repo jleechanorg/smartc...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #6: docs: add OpenClaw Docker staging setup guide — adds `/Users/jleechan/repos/smartclaw/docs/openclaw-docker-staging-setup.md` and claims to provide a complete Docker st...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state including reviews, body, and check for design doc / evidence secti...

6. @coderabbitai all good?

7. @coderabbitai all good?

8. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state
gh pr view 6 --repo jleechanorg/smartclaw --json state,mergeable,mergeStateStatus,reviews,title,headRefName

echo "---COMMIT_COUNT---"
gh ...

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state
gh pr view 6 --repo jleechanorg/smartclaw --json state,mergeable...

10. @coderabbitai all good?

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state
gh pr view 6 --repo jleechanorg/smartclaw --json state,mergeable...

12. @coderabbitai all good?

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state
gh pr view 6 --repo jleechanorg/smartclaw --json state,mergeable,m...

14. @coderabbitai review — all prior review threads are resolved; please re-review for approval.

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state
gh pr view 6 --repo jleechanorg/smartclaw --json state,mergeable,m...

16. @coderabbitai all good?

17. @coderabbitai all good?

18. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR state
gh pr view 6 --repo jleechanorg/smartclaw --json state,mergeable,m...

19. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 6 --repo jleechanorg/smartclaw --json state,mergeable,mergeStateStatus,reviews...

