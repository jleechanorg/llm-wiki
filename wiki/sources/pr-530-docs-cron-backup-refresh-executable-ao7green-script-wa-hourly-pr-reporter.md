---
title: "docs: cron backup refresh, executable ao7green script, WA hourly PR reporter"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-07
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/530
pr_number: 530
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary

- **`docs/context/CRON_JOBS_BACKUP.md`** — Refreshed export of gateway cron job definitions (schedules, descriptions, last-run notes) for ops visibility and drift tracking.
- **`scripts/ao7green-pr-monitor.launchd.sh`** — Mark executable (`100755`) so launchd/helpers can run it without a shell workaround.
- **`workspace/AGENTS.md`** — Adds the same “AO worker first for local flows” guidance as root `AGENTS.md` for sessions whose CWD is `workspace/`.
- **`scripts/worldarchitect-hourly...

## Key Changes
- 4 commit(s) in this PR
- 7 file(s) changed

- Merged: 2026-04-07

## Commit Messages
1. docs: refresh cron jobs backup; chmod +x ao7green monitor; add WA hourly PR script
  
  - Re-export CRON_JOBS_BACKUP.md with schedules and last-run context
  - Make ao7green-pr-monitor.launchd.sh executable for launchd/helpers
  - Mirror AO-worker-first note in workspace AGENTS.md
  - Add worldarchitect-hourly-pr-report.sh for hourly #worldai PR summaries
  
  Made-with: Cursor
2. fix: correct jq variable injection in worldarchitect-hourly-pr-report.sh
  
  CodeRabbit flagged 3 critical bugs:
  - jq -rn "\$raw | .total_count" passed shell vars as filter string
    instead of JSON input — fixed with heredoc <<<"\$raw"
  - Same pattern on lines 31-37 for .number, .state, .draft, .head.sha
  - Malformed JSON in Slack API call — fixed with jq -n --arg
  
  Also fixes 4 doc inconsistencies in CRON_JOBS_BACKUP.md:
  - ao:primary-5m- → ao:primary-60m- (schedule is hourly)
  - clawchief:daily-task-prep: 0 2 * * * → 0 2 * * 1-5 (weekdays)
  - life:daily-important-email-calendar-8am → -9am (cron is 9am)
  - life:renew-car-registration-hourly → -weekly (schedule is Friday)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
3. fix: cron backup fidelity, worldarchitect jq, dead code
  
  - cron-backup-sync.sh: preserve schedule.kind/expr/everyMs in JSON
    backup; add schedule+description to markdown generator
  - worldarchitect-hourly-pr-report.sh: fix jq -rn ignoring stdin in
    fallback path (total_count was always 0); remove dead status_icon
    assignment; update comment to remove "mock" misnomer
  - Regenerate CRON_JOBS_BACKUP.{json,md,html} with all 13 jobs and
    correct schedule/description fields
  
  Note: several live cron job names have schedule/name mismatches
  ( ao:primary-5m-drive-to-7-green is every 60m, life:renew-car-registration-
    hourly is weekly Friday 9am, clawchief:daily-task-prep cron is daily
    not weekdays-only ) — these are live config issues outside this PR scope.
4. fix: preserve tz in cron backup, add is:open to search query
  
  - cron-backup-sync.sh: include tz/anchorMs/staggerMs in schedule allowlist
    so timezone and stagger settings are preserved in backup JSON
  - worldarchitect-hourly-pr-report.sh: add is:open to search query so
    total_count excludes closed/merged PRs; captured tz in schedule field
  - Regenerate CRON_JOBS_BACKUP.{json,md,html} with live state (14 jobs
    including new "Oren business setup" job, all schedules complete)

## Files Changed
- `docs/context/CRON_JOBS_BACKUP.html`
- `docs/context/CRON_JOBS_BACKUP.json`
- `docs/context/CRON_JOBS_BACKUP.md`
- `scripts/ao7green-pr-monitor.launchd.sh`
- `scripts/cron-backup-sync.sh`
- `scripts/worldarchitect-hourly-pr-report.sh`
- `workspace/AGENTS.md`

## Review Notes
1. @coderabbitai all good?

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **4...

3. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions`[bot] I'll do a fresh review of the PR now to give you a proper status assessment!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review a...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec -
Error loading config.toml: env is not supported for streamable_http
in `mcp_servers.perplexity-ask`

. C...

5. @coderabbitai all good?

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions` Yes, this PR looks good overall! Here's a quick summary of the status:

**✅ What's clean:**
- **`scripts/worldarchitect-hourly-pr-report.sh`** — Tokens a...

8. <!-- This is an auto-generated reply by CodeRabbit -->
`@jleechan2015` — looking good overall! The Skeptic Agent `FAIL` was a **pure infrastructure issue** (Codex MCP config error + Claude unavailable), not a reflection of the PR's code quality.

Here's a quick sanity check on the four changed areas...

9. @coderabbitai all good?

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions` Yes, the PR looks good! Here's the quick status:

| File | Status | Notes |
|---|---|---|
| `docs/context/CRON_JOBS_BACKUP.md` | ✅ | Docs-only refresh, n...

11. @coderabbitai all good?

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Yes, still all good! ✅ Nothing has changed since the last checks:

| File | Status |
|---|---|
| `docs/context/CRON_JOBS_BACKUP.md` | ✅ Docs refresh, no ...

13. @coderabbitai all good?

14. @coderabbitai all good?

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Yes, still all good! ✅ Status unchanged from previous checks:

| File | Status |
|---|---|
| `docs/context/CRON_JOBS_BACKUP.md` | ✅ Docs refresh, no conc...

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions` — Yes, still all good! ✅ This PR has been reviewed multiple times with no new changes:

| File | Status |
|---|---|
| `docs/context/CRON_JOBS_BACKUP.md` ...

17. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

18. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, checks, and review comments
echo "=== PR STATUS ==="
gh pr view 530 --re...

19. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

20. ## PR is green (7/7 criteria met — awaiting auto-merge)

| # | Criterion | Status |
|---|-----------|--------|
| 1 | CI green | PASS — Skeptic:  |
| 2 | No conflicts | PASS —  |
| 3 | CR APPROVED | PASS — coderabbitai APPROVED (commit=null, post-fixes) |
| 4 | Bugbot clean | PASS —  |
| 5 | Comments...

