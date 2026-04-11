---
title: "feat: mem0 embedding fix, minimax config tests, docs, AO progress"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-06
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/517
pr_number: 517
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary
Bundles harness improvements that were pending on `main` working tree (targeted `git add` only — no workspace screenshots).

### Included
- **mem0**: `scripts/mem0_shared_client.py` — pass OpenAI `dimensions` for 768-d Qdrant collections; `check_compatibility=false` for qdrant-client. Unit tests in `src/tests/test_mem0_shared_client.py`.
- **openclaw-mem0 plugin**: postinstall patch for upstream mem0ai OpenAI embedder (`dimensions: this.embeddingDims`); vitest for patch idempotency; `...

## Key Changes
- 3 commit(s) in this PR
- 10 file(s) changed

- Merged: 2026-04-06

## Commit Messages
1. feat: mem0 embedding fix, minimax docs, AO progress reporter, minimax doctor tests
  
  - mem0_shared_client: OpenAI dimensions + Qdrant check_compatibility; tests
  - openclaw-mem0: postinstall patch for mem0ai OpenAI embed dimensions (768)
  - CLAUDE.md + openclaw-models skill: minimax-portal primary, timeout bounds
  - test_openclaw_configs: TestMinimaxProviderConsistency (plugins + model ids)
  - agent-orchestrator.yaml + ao-progress-reporter.sh: related harness updates
  
  Made-with: Cursor
2. fix: ao-progress-reporter.sh 4 bugs found by code review bots
  
  - ao_sessions_json: restore fetch_ao_sessions() call before use (set -u fix)
  - thread_ts: export SLACK_THREAD_TS after resolve so post_slack uses it
  - DRY_RUN: skip Slack post in resolve_thread_ts when DRY_RUN=1
  - thread_ts empty: only include in Slack JSON payload when non-empty
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
3. fix: redirect log() to stderr to keep resolve_thread_ts stdout pure
  
  log() was writing to stdout, polluting the command substitution
  return value of resolve_thread_ts. Now uses >&2 so only the
  function's echo "$thread_ts" goes to stdout.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `.claude/skills/openclaw-models.md`
- `CLAUDE.md`
- `agent-orchestrator.yaml`
- `extensions/openclaw-mem0/package.json`
- `extensions/openclaw-mem0/scripts/patch-mem0ai-openai-embeddims.mjs`
- `extensions/openclaw-mem0/scripts/patch-mem0ai-openai-embeddims.test.ts`
- `scripts/ao-progress-reporter.sh`
- `scripts/mem0_shared_client.py`
- `src/tests/test_mem0_shared_client.py`
- `tests/test_openclaw_configs.py`

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
# Check the ao-progress-reporter.sh for the ao_sessions_json usage
fd -i "ao-progress-rep...

4. ## Hourly Monitor Cycle — 2026-04-06T05:12 UTC

**Open PRs: 1**

| # | Condition | Status |
|---|-----------|--------|
| 1 | CI green | ⏳ No check runs recorded yet (PR is ~2 min old) |
| 2 | Mergeable | ❌ `unstable` |
| 3 | CR APPROVED | ❌ Rate-limited — review pending |
| 4 | Bugbot clean | ⚠️ Cod...

5. @coderabbitai all good?

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me check the current state of the script to confirm whether the bug has been addressed.

---

🏁 Script executed:
```
#!/...

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check whether fetch_ao_sessions is now called in the main block
fd -i "ao-progress-repo...

9. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, CI checks, merge status
gh pr view 517 --repo jleechanorg/jleechanclaw -...

11. @coderabbitai all good?

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 517 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

13. @coderabbitai all good?

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 517 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

15. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

16. ✅ PR is green (7/7 criteria met — awaiting auto-merge)

| # | Condition | Status |
|---|-----------|--------|
| 1 | CI green (Staging Canary + Skeptic Gate) | ✅ PASS |
| 2 | No conflicts (mergeable_state=clean) | ✅ PASS |
| 3 | CR APPROVED (coderabbitai[bot]) | ✅ PASS |
| 4 | Bugbot clean (cursor[bo...

