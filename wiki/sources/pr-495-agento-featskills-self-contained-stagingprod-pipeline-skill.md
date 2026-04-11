---
title: "[agento] feat(skills): self-contained staging→prod pipeline skill"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-04
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/495
pr_number: 495
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
The OpenClaw staging→production deployment pipeline is spread across multiple scripts (deploy.sh, staging-canary.sh, gateway-preflight.sh, install-launchagents.sh), launchd plist templates, and CLAUDE.md sections. A new machine setting up from scratch had no single place to reference — the knowledge was implicit in the code and incident history.

## Goals
Create a self-contained, portable skill that documents the complete staging→prod pipeline so any agent or human can install, ope...

## Key Changes
- 2 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-04

## Commit Messages
1. feat(skills): add self-contained staging→prod pipeline skill
  
  Documents the full OpenClaw staging→production deployment pipeline
  including architecture, install steps, deploy procedure, canary
  verification, rollback, troubleshooting, and maintenance.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
2. [copilot] fix: address 7 Copilot inline comment accuracy issues in SKILL.md
  
  - Deploy flow: correct --fix flag vs no-flag for gateway-preflight.sh step 1
  - Rollback: remove false claim deploy.sh creates .bak; use staging copy or git restore
  - plist binary: fix attribution — openclaw CLI misreads binary plists, not launchd
  - NODE_MODVER: correct Step 6 to record only one baseline file (install-launchagents.sh handles prod)
  - Duplicate plists: clarify both com.openclaw.gateway + ai.openclaw.staging must coexist
  - monitor-agent: correct interval 30min→1hr (StartInterval=3600 in plist)
  - Key paths: correct .bak file description (rotating install backup, not deploy.sh)
  - Prerequisites table: correct remote requirement to jleechanorg/jleechanclaw
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `.claude/skills/staging-prod-pipeline/SKILL.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **3...

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
`@jleechan2015` Let me take a proper look at the PR and get back to you with a full review!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already r...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL

## Background
PR [495](https://github.com/jleechanorg/jleechanclaw/pull/495): feat(skills): self-contained staging→prod pipeline skill — claims to add a portable `.claude` s...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get the PR diff and file content
gh pr view 495 --repo jleechanorg/jleechanclaw --json ...

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — My full analysis is already posted above in this thread, but to summarize my position cleanly:

**I agree with the skeptic on process gates; content is t...

7. @codex @coderabbitai @cursor @copilot [AI automation] Codex will implement the code updates while coderabbitai, cursor, and copilot focus on review support. Please make the following changes to this PR.

**Summary (Execution Flow):**
1. Review every outstanding PR comment to understand required fixe...

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fetch all review comments on PR `#495`
gh api repos/jleechanorg/jleechanclaw/pulls/495/...

9. ## Hourly Monitor Cycle — 2026-04-04T19:15Z

- **Open PRs**: 2
- **7-green merges**: 0
- **Stuck PRs (>48h)**: none
- **CI failures**: PR #495 Skeptic Gate (VERDICT: FAIL)
- **Issues created**: none
- **Next action**: See below — both PRs need human attention

---

### PR Status

```
PR #495 — age: ...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Acknowledged. Here's my status update in response to the monitor cycle:

---

### PR `#495` Gate Status — CodeRabbit Response

**Gate 3 (CR APPROVED):** ...

11. @coderabbitai all good?

12. [AI responder]
## Copilot Response - All Comments Addressed

**Coverage:** 11/11 comments addressed (7 fixed, 4 acknowledged)
**This run:** 11 new, 0 carried forward
**Files modified:** .claude/skills/staging-prod-pipeline/SKILL.md
**CI status:** unstable (in_progress — all checks pending)

### CRIT...

13. @coderabbitai all good?

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 495 --repo jleechanorg/jleechanclaw --json state,merge...

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me do a quick verification of the current state before answering.

---

🏁 Script executed:
```
#!/bin/bash
# Get current...

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
gh pr view 495 --repo jleechanorg/jleechanclaw \
  --json state,...

18. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

19. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR [#495](https://github.com/jleechanorg/jleechanclaw/pull/495): [agento] feat(skills): self-contained staging→prod pipeline skill — adds a new self-contained deploy/runbook ...

20. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 495 --repo jleechanorg/jleechanclaw \
  --json state,...

21. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

22. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 495 --repo jleechanorg/jleechanclaw \
  --json state,...

