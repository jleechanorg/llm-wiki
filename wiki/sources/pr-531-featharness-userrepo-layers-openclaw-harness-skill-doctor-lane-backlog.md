---
title: "feat(harness): user/repo layers, openclaw-harness skill, doctor lane backlog"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-09
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/531
pr_number: 531
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary

- **User vs repository harness:** Tracked copies under `docs/harness/` (`user-command-harness.md`, scope snippet for `harness-engineering`) plus `scripts/sync-harness-user-scope.sh` to sync the global `/harness` command from the repo after `git pull`.
- **Repo-local:** New `.claude/skills/openclaw-harness/SKILL.md` and expanded `.claude/commands/harness.md` overlay (OpenClaw gateway, canary, deploy, collision rule).

**Note:** `~/.claude/commands/harness.md` and `~/.claude/skills/har...

## Key Changes
- 5 commit(s) in this PR
- 9 file(s) changed

- Merged: 2026-04-09

## Commit Messages
1. docs: refresh cron jobs backup; chmod +x ao7green monitor; add WA hourly PR script
  
  - Re-export CRON_JOBS_BACKUP.md with schedules and last-run context
  - Make ao7green-pr-monitor.launchd.sh executable for launchd/helpers
  - Mirror AO-worker-first note in workspace AGENTS.md
  - Add worldarchitect-hourly-pr-report.sh for hourly #worldai PR summaries
  
  Made-with: Cursor
2. feat(harness): user/repo layers, openclaw-harness skill, doctor lane backlog
  
  - Add openclaw-harness skill and expand repo-local /harness command with sync pointers
  - Track user-scope command + skill snippet under docs/harness/; add sync script
  - doctor.sh: warn on recent gateway.err.log lane wait exceeded (parity with CLAUDE.md)
  - CLAUDE.md: document lane backlog in doctor/monitor parity rule
  
  Made-with: Cursor
3. chore: gitignore mcp-daemon (fleet lives in ~/.config, user_scope backup)
  
  Made-with: Cursor
4. fix: address PR 531 review — lane backlog in staging-canary, Slack JSON, harness docs
  
  Made-with: Cursor
5. fix: lane backlog check 9 fails on detected issue; Slack JSON payload uses proper jq -n encoding

## Files Changed
- `.claude/skills/openclaw-harness/SKILL.md`
- `.gitignore`
- `docs/harness/README.md`
- `docs/harness/harness-engineering-scope-snippet.md`
- `docs/harness/index.html`
- `docs/harness/user-command-harness.md`
- `scripts/doctor.sh`
- `scripts/sync-harness-user-scope.sh`
- `scripts/worldarchitect-hourly-pr-report.sh`

## Review Notes
1. @coderabbitai all good?

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- walkthrough_start -->

<details>
<summary>📝 Walkthrough</summary>

## Walkthrough

This pull request adds comprehensive harness documentation establishing a layering model between user-scope and repository-local harness arti...

3. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions`[bot]: I'll do a fresh review of the PR to check if everything looks good!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already r...

4. @coderabbitai all good?

5. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions` Let me run a fresh review of the PR to give you an accurate status update!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already ...

6. ## Hourly Monitor Cycle — 2026-04-07T02:15 UTC

- Open PRs: 3 (#529, #530, #531)
- 7-green merges: 0
- Stuck PRs (>48h): none (all created 2026-04-06 or 2026-04-07)
- CI failures on main: none (last 5 commits all clean)
- Actions taken: none (monitor only)

---

### PR #530 — docs: cron backup refre...

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
# Get PR `#531` details
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,merge...

9. ## Hourly Monitor Cycle — 2026-04-07 03:05 UTC

- Open PRs: 3 (#529, #530, #531)
- 7-green merges: 0 (no admin-merge performed — skeptic-cron.yml handles auto-merge)
- Stuck PRs (>48h): none (all created 2026-04-06 or 2026-04-07)
- CI failures on main: none detected
- Issues created: none
- Next act...

10. @coderabbitai all good?

11. @coderabbitai all good?

12. @coderabbitai all good? (pushed fb344a465f — comment tweak on staging-canary)

13. @coderabbitai all good?

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,stat...

15. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get latest PR `#531` status
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,mergeable,isDraft,reviewDecision,statusCheckRollup,reviews 2>/dev/null | ...

16. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR `#531` state
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,mergeable,isDraft,reviewDecision,statusCheckRollup,headRefOid,commits 2>/...

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR `#531` status
gh pr view 531 --repo jleechanorg/jleechanclaw --json stat...

18. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

19. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

20. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR `#531` status
gh pr view 531 --repo jleechanorg/jleechanclaw --json stat...

21. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #531: feat(harness): user/repo layers, openclaw-harness skill, doctor lane backlog — claims to add tracked user-vs-repository harness docs, a new `openclaw-harness` skill ...

22. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR `#531` review state
gh pr view 531 --repo jleechanorg/jleechanclaw --jso...

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Responding to the Skeptic consultation. Here is my confirmation and one important correction:

---

### ✅ Confirmed: Overall FAIL verdict is correct

All...

24. <!-- This is an auto-generated reply by CodeRabbit -->
### Rate Limit Exceeded

`@jleechan2015` have exceeded the limit for the number of chat messages per hour. Please wait **0 minutes and 31 seconds** before sending another message.

25. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,stat...

26. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,stat...

27. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,stat...

28. @coderabbitai all good?

29. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,stat...

30. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

31. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR `#531` status
gh pr view 531 --repo jleechanorg/jleechanclaw --json stat...

32. @coderabbitai all good?

33. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 531 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,stat...

