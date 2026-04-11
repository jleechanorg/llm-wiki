---
title: "chore: sync beads, mem0 recall, monitor PATH, AO workspace policy"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-05
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/515
pr_number: 515
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary
Syncs harness state and small operational tweaks.

## Changes
- **Beads** (`.beads/issues.jsonl`): issue closes/opens and new orch items.
- **mem0 recall** (`.claude/hooks/mem0_recall.py`): `TOP_K` 6→4, `SCORE_THRESHOLD` 0.35→0.45 (fewer, higher-confidence chunks).
- **monitor-agent** (`monitor-agent.sh`): prepend `$HOME/.nvm/versions/node/v22.22.0/bin` to `PATH` so OpenClaw uses Node 22 before Homebrew.
- **AO** (`agent-orchestrator.yaml`): remove `evolveLoop` block under the claw pr...

## Key Changes
- 2 commit(s) in this PR
- 10 file(s) changed

- Merged: 2026-04-05

## Commit Messages
1. chore: sync beads, tighten mem0 recall, monitor PATH, AO config
  
  - .beads/issues.jsonl: close/open orch issues and new follow-ups
  - mem0_recall: TOP_K 6→4, SCORE_THRESHOLD 0.35→0.45
  - monitor-agent.sh: prepend nvm Node v22.22.0 bin to PATH (ABI alignment)
  - agent-orchestrator: remove evolveLoop block from claw project
  - docs/context/DOC_GAPS.md: regenerate timestamp
  - memory/mcp-mail-ack-log.md: append recent ack lines
  - workspace MEMORY/SOUL: refresh project status and learned patterns
  
  Made-with: Cursor
2. fix(doctor): add plugins.slots.memory config guard + protected key
  
  mem0 was silently disabled because plugins.slots.memory was unset,
  causing gateway to default to builtin memory-core. Added:
  - doctor.sh check 4a: validates plugins.slots.memory == "openclaw-mem0"
  - CLAUDE.md protected keys table: plugins.slots.memory entry
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `.beads/issues.jsonl`
- `.claude/hooks/mem0_recall.py`
- `CLAUDE.md`
- `agent-orchestrator.yaml`
- `docs/context/DOC_GAPS.md`
- `memory/mcp-mail-ack-log.md`
- `monitor-agent.sh`
- `scripts/doctor.sh`
- `workspace/MEMORY.md`
- `workspace/SOUL.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **0...

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Overall the PR looks clean — here's a quick rundown:

| File | Risk | Notes |
|---|---|---|
| `.claude/hooks/mem0_recall.py` | Low | `TOP_K` 6→4, `S...

4. ## Hourly Monitor Cycle — 2026-04-05 21:25 UTC

- Open PRs: 1 (PR #515)
- 7-green merges: 0
- Stuck PRs (>48h): none
- CI failures: Skeptic Gate — VERDICT: FAIL
- Issues created: none

### PR #515 — age: 0h 12m — status: concerning

**7-Green Gate Status:**

| # | Gate | Result | Detail |
|---|-----...

5. @coderabbitai all good?

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Not quite — PR `#515` has **3 blocking gates** that need to clear before it's merge-ready:

| Gate | Status | What's needed |
|---|---|---|
| **CR A...

7. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, reviews, checks, and comments
gh pr view 515 --repo jleechanorg/jleechan...

9. @coderabbitai I dismissed the CHANGES_REQUESTED because all comments are non-blocking: (1) DOC_GAPS.html does not exist in the base — no paired HTML to update, (2) node/current/bin does not exist on this system so prepending v22.22.0/bin is the correct approach per CLAUDE.md, (3) isolated gateway te...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR state/reviews
gh pr view 515 --repo jleechanorg/jleechanclaw --json st...

11. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | FAIL | state=none...

12. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #515: chore: sync beads, mem0 recall, monitor PATH, AO workspace policy — syncs harness state with operational tweaks (mem0 thresholds, Node PATH in monitor-agent, evolveL...

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR review state
gh pr view 515 --repo jleechanorg/jleechanclaw --json sta...

14. @coderabbitai Please re-review. The CHANGES_REQUESTED was dismissed because your comments were non-blocking (paired HTML does not exist in base, node/current symlink absent on this system). All CI checks pass and the PR is ready to merge. Please post APPROVED or CHANGES_REQUESTED.

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 515 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,revi...

16. @coderabbitai all good?

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 515 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,revi...

