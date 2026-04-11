---
title: "[agento] feat(skills): add executive-assistant skills + fix script flags and doctor.sh"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-04
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/496
pr_number: 496
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
Local uncommitted changes accumulated across sessions: 6 new executive-assistant skills, two script fixes, and a workspace task list update.

## Goals
- Ship the 6 executive-assistant skills to the repo
- Fix the --timeout-seconds flag regression in daily-openclaw-research.sh
- Clean up stale gateway cron UUIDs from doctor.sh; harden mem0-disabled path to fail

## Tenets
- Minimal scope — no unrelated refactors

## High-level description of changes
- 6 new skills: action-items-todo...

## Key Changes
- 2 commit(s) in this PR
- 13 file(s) changed

- Merged: 2026-04-04

## Commit Messages
1. [agento] feat(skills): add executive-assistant skills + fix script flags and doctor.sh
  
  - Add 6 new skills: action-items-todoist, email-drafting, executive-digest,
    humanizer, meeting-prep, todoist-due-drafts (+ skills-executive-assistant-config/)
  - fix(scripts): daily-openclaw-research.sh: --timeout-seconds → --timeout (correct flag)
  - fix(doctor.sh): remove stale gateway cron UUIDs; warn→fail for disabled mem0 plugin
  - chore(workspace): update current.md timestamp and appointment time
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
2. fix(skills): address PR review findings — path refs, config fields, setup numbering
  
  - doctor.sh: fix stale comment (mem0 disabled is a failure, not 'not an error')
  - All SKILL.md files: use absolute ~/executive-assistant-skills/config/user.json
    instead of relative ../config/user.json (ambiguous when deployed under skills/)
  - Skill cross-references: add missing skills/ subdirectory prefix to all paths
  - crons.md: fix skill paths to include skills/ prefix
  - user.example.json: add scheduling_cc_name and chief_of_staff fields
  - email-drafting SKILL.md: add workspace and scheduling_cc_name to required config
  - meeting-prep SKILL.md: add chief_of_staff.name/.slack_dm_channel to config
  - setup.md: renumber duplicate ## 5 → ## 6 and shift subsequent sections;
    fix broken gog reference (workspace/skills/gog/SKILL.md does not exist)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `scripts/daily-openclaw-research.sh`
- `scripts/doctor.sh`
- `skills-executive-assistant-config/config/DEBUG_LOGGING.md`
- `skills-executive-assistant-config/config/user.example.json`
- `skills-executive-assistant-config/docs/crons.md`
- `skills-executive-assistant-config/docs/setup.md`
- `skills/action-items-todoist/SKILL.md`
- `skills/email-drafting/SKILL.md`
- `skills/executive-assistant/executive-digest/SKILL.md`
- `skills/humanizer/SKILL.md`
- `skills/meeting-prep/SKILL.md`
- `skills/todoist-due-drafts/SKILL.md`
- `workspace/tasks/current.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **6...

2. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #496: [agento] feat(skills): add executive-assistant skills + fix script flags and doctor.sh — claims to add six executive-assistant skills, migrate cron/health-check beha...

3. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

4. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

Let me check the actual PR state to give an informed response.

---

🏁 Script executed:
```
#!/bin/bash
# Get PR details and files changed
gh pr view 496 --repo jleechanorg/jleechanclaw --json state...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR details, reviews, status checks, and comments
echo "=== PR STATUS ==="
gh pr vie...

6. ## Hourly Monitor Cycle — 2026-04-04T22:10Z

- Open PRs: 1
- 7-green merges: 0
- Stuck PRs (>48h): none (PR #496 is ~15 min old)
- CI failures: Skeptic Gate — VERDICT: FAIL (previous run); new Skeptic Gate run in_progress
- Issues created: none

### PR #496 — age: 0h 15m — status: concerning

**Titl...

7. @coderabbitai all good?

8. @coderabbitai all good?

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 496 --repo jleechanorg/jleechanclaw --json state,merg...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Quick current state check for PR `#496`
echo "=== REVIEW DECISION ==="
gh pr view 496 -...

11. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #496: [agento] feat(skills): add executive-assistant skills + fix script flags and doctor.sh — claims it ships six executive-assistant skills, documents setup/crons, fixes...

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 496 --repo jleechanorg/jleechanclaw --json state,merg...

13. @coderabbitai approve

14. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Comments resolved and changes approved.

</details>

15. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 496 --repo jleechanorg/jleechanclaw --json state,merg...

17. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

