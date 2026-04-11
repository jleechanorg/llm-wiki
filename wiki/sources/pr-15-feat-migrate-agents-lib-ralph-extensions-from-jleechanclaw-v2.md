---
title: "feat: migrate agents, lib, ralph, extensions from jleechanclaw (v2)"
type: source
tags: [github, pr, jleechanorg-smartclaw]
sources: []
date: 2026-04-10
pr_url: https://github.com/jleechanorg/smartclaw/pull/15
pr_number: 15
pr_repo: jleechanorg/smartclaw
---

## Summary
## Summary
Re-attempt of PR #14 with portability fixes applied

- Migrate canonical agent configs (agents/)
- Migrate shared shell library (lib/)
- Migrate Ralph automation (ralph/)
- Migrate mem0 extension (extensions/openclaw-mem0/)
- Migrate operational scripts (scripts/*.sh)
- Apply portability fixes: replace hardcoded /Users/jleechan with $HOME

## Why
Consolidate into smartclaw as canonical home. jleechanclaw pulls from smartclaw.

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---...

## Key Changes
- 1 commit(s) in this PR
- 2 file(s) changed

- Merged: 2026-04-10

## Commit Messages
1. fix: apply portability fixes from jleechanclaw PR #538

## Files Changed
- `scripts/install-openclaw-launchd.sh`
- `scripts/openclaw-upgrade-safe.sh`

## Review Notes
1. @coderabbitai all good?

2. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```7d0cdb1```_
<!-- HEAD-SHA: 7d0cdb123305db5c8ee6deaaeeedbb8b44b2cf16 -->

3. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- walkthrough_start -->

<details>
<summary>📝 Walkthrough</summary>

## Walkthrough

Multiple shell scripts were updated to rebrand from the `smartclaw` namespace to the `openclaw` namespace. Changes include updating launchd s...

4. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```7d0cdb1```_
<!-- HEAD-SHA: 7d0cdb123305db5c8ee6deaaeeedbb8b44b2cf16 -->

5. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```7d0cdb1```_
<!-- HEAD-SHA: 7d0cdb123305db5c8ee6deaaeeedbb8b44b2cf16 -->

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR details, status checks, and review comments
gh pr view 15 --repo jleechanorg/sma...

7. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```7d0cdb1```_
<!-- HEAD-SHA: 7d0cdb123305db5c8ee6deaaeeedbb8b44b2cf16 -->

8. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 15 --repo jleechanorg/smartclaw --json title,state,me...

10. @coderabbitai all good?

11. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```1b39138```_
<!-- HEAD-SHA: 1b39138ab9995f155384bc08cbfd9df874810ca6 -->

12. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```1b39138```_
<!-- HEAD-SHA: 1b39138ab9995f155384bc08cbfd9df874810ca6 -->

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 15 --repo jleechanorg/smartclaw --json title,state,me...

