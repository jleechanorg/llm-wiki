---
title: "[agento] feat: add ZFC rule to agentRules in agent-orchestrator.yaml"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-05
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/504
pr_number: 504
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background

Steve Yegge's Zero-Framework Cognition (ZFC) principle: applications should be thin deterministic shells that delegate ALL judgment, classification, routing, and ranking to AI model calls — never implement heuristics, keyword matching, semantic scoring, or routing logic in application code.

A search of all local branches, PRs, CLAUDE.md, AGENTS.md, and openclaw config found ZERO enforcement of ZFC existed anywhere. This PR adds it to the AO worker agentRules in agent-orchestrator...

## Key Changes
- 3 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-05

## Commit Messages
1. [agento] feat: add ZFC rule to agentRules in agent-orchestrator.yaml
2. [agento] fix: escape embedded double quotes in YAML scalar
3. [agento] fix: add ZFC rule to all project agentRules overrides (cursor[bot] review)

## Files Changed
- `agent-orchestrator.yaml`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **1...

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Look at the changed files in the PR
git diff HEAD~1 HEAD --name-only
git diff HEAD~1 HE...

4. @coderabbitai all good?

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Yes, all good! ✅ This is a clean, configuration-only change that appends the ZFC rule to `defaults.agentRules` in `agent-orchestrator.yaml`. No stru...

6. @coderabbitai all good?

7. @coderabbitai all good?

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions` Yes, all good! ✅ This is a clean, configuration-only change that appends the ZFC rule to `defaults.agentRules` in `agent-orchestrator.yaml`. No structura...

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` Yes, still all good! ✅ The PR is a clean, configuration-only change — no issues to flag. The ZFC rule is correctly appended to `defaults.agentRules` with c...

10. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, CI checks, and mergeable state
gh pr view 504 --repo jleechanorg/jleecha...

12. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

13. PR is green (6/6 criteria met — Staging Canary Gate PASS, Staging Canary Full PASS, Skeptic Gate PASS, CR APPROVED, mergeable, cursor[bot] Medium + chatgpt P0 resolved and documented). Awaiting auto-merge.

14. PR #504 is green (7/7 criteria met — awaiting auto-merge)

