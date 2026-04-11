---
title: "fix(monitor): Slack E2E matrix harness fixes + staging config repair + skeptic webhook"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-10
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/539
pr_number: 539
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary

- **monitor-agent.sh**: Fix 4 bugs causing false-red STATUS=PROBLEM on every matrix run:
  1. Sender token precedence — `SLACK_USER_TOKEN` (human xoxp) now wins over `OPENCLAW_SLACK_USER_TOKEN` (bot-scoped)
  2. Timeout too short — `SLACK_E2E_TIMEOUT_SECONDS` now defaults to 180s (replies arrive 25-160s after probe)
  3. RUN_CANARY gate — matrix was gated behind `if [ "$RUN_CANARY" = "1" ]`, silently disabling it; gate removed
  4. Bot-authored sender detection — `slack_post_message_...

## Key Changes
- 5 commit(s) in this PR
- 11 file(s) changed

- Merged: 2026-04-10

## Commit Messages
1. add skeptic webhook trigger and coverage diagnostics
2. chore: small harness followups — mem0 graceful degradation, doctor parity, bead/doc updates
  
  - extensions/openclaw-mem0/index.ts: degrade add() to no-op on ZodError/structured-output parse failures instead of crashing
  - CLAUDE.md: doc update from prior session
  - launchd/ai.openclaw.schedule.pr-monitor-worldai.plist: add worldai PR monitor plist
  - .beads/issues.jsonl, workspace/MEMORY.md, extensions/openclaw-mem0/README.md: housekeeping
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
3. fix(monitor): Slack E2E matrix harness — sender token, timeout, RUN_CANARY gate, bot-sender guard
  
  Root causes of false-red STATUS=PROBLEM verdicts on both staging and prod:
  
  1. Sender token precedence: monitor preferred OPENCLAW_SLACK_USER_TOKEN (bot-scoped on this machine) over SLACK_USER_TOKEN (real human xoxp token). Swapped precedence so human token wins.
  
  2. Timeout too short: SLACK_E2E_TIMEOUT_SECONDS was inheriting from CANARY_TIMEOUT_SECONDS (~45s). Real replies arrive 25-160s after probe. Changed default to 180s (override via env).
  
  3. RUN_CANARY gate: run_slack_e2e_matrix_probe was gated behind `if [ "$RUN_CANARY" = "1" ]`, so disabling the legacy canary also silently disabled the six-mode matrix. Removed the gate — matrix now always runs.
  
  4. Bot-authored sender detection: top-level channel_no_mention probes posted by a bot/app identity will never get a reply. Added slack_post_message_author_kind() that flags these as invalid_sender_{bot,app} (rc=7) rather than a product failure.
  
  5. install-launchagents.sh: staging overlay generator now forces gateway.port=18810, keeps Slack enabled (needed by canary/monitor), and removes unsupported stagingDerivedFrom metadata key.
  
  6. doctor.sh: adds check_shared_slack_socket_tokens() to warn when staging and prod share the same Slack tokens (causes event-loop cross-talk).
  
  Tests: 19/19 shell regressions pass, 50/50 pytest slice passes.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
4. fix(pr539): address CR review — scope mem0 degradation to auto-capture, gate invalid_sender on resolved user-id, legacy prod label check, token CLI exposure, skeptic trigger regex
  
  - extensions/openclaw-mem0/index.ts: scope isMem0OssStructuredOutputError degradation
    to auto-capture path only (autoCapture flag); explicit memory_store writes now
    propagate errors instead of silently returning empty results
  - monitor-agent.sh: gate invalid_sender_* classification on non-empty sender_user_id
    to avoid false positives when auth.test fails
  - scripts/doctor.sh: check legacy com.openclaw.gateway label in addition to
    ai.openclaw.gateway when probing prod side of shared-token collision
  - scripts/install-launchagents.sh: remove Slack tokens from python3 argv; read from
    env only to avoid secrets in process list
  - src/orchestration/webhook.py: fix _trigger_type_for to use _SKEPTIC_TRIGGER_SHA_RE
    regex instead of literal SKEPTIC_CRON_TRIGGER string (aligns with SHA extractor)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. fix: remaining review items — trusted actor gate, bot-marker ordering, auth.test dedup
  
  - webhook: restrict skeptic trigger to trusted actors only
    (github-actions[bot], jleechan, jleechanao) to prevent untrusted
    commenters from enqueuing expensive skeptic runs
  - webhook: also accept literal SKEPTIC_CRON_TRIGGER alongside SHA regex
    for robustness
  - monitor: check bot_id/app_id before user-id match in
    slack_post_message_author_kind to prevent false-green when xoxb
    token shares user ID with bot
  - monitor: deduplicate auth.test curl by having
    resolve_primary_bot_user_id delegate to resolve_slack_token_user_id
  
  Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

## Files Changed
- `.beads/issues.jsonl`
- `CLAUDE.md`
- `extensions/openclaw-mem0/index.ts`
- `monitor-agent.sh`
- `scripts/check-pr-worker-coverage.sh`
- `scripts/doctor.sh`
- `scripts/install-launchagents.sh`
- `src/orchestration/webhook.py`
- `tests/test_monitor_slack_e2e_matrix.sh`
- `tests/test_openclaw_configs.py`
- `workspace/MEMORY.md`

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

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check key files mentioned in the PR
echo "=== webhook.py (skeptic trigger section) ==="...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -
OpenAI Codex v0.117.0 (research preview)
--------
workdir: /Users/jleechan/projects/jlee...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — The skeptic agent's FAIL was an **infrastructure failure** (Codex exhausted its usage credits before completing any analysis), so there is no substantive...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current PR status
gh pr view 539 --repo jleechanorg/jleechanclaw --json state,isD...

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
echo "=== PR Current State ==="
gh pr view 539 --repo jleechanorg/jleechanclaw --json sta...

10. @coderabbitai approve

11. @coderabbitai all good?

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR Current State ==="
gh pr view 539 --repo jleechanorg/jleechanclaw --json sta...

13. @coderabbitai all good?

14. @coderabbitai all good?

15. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Comments resolved and changes approved.

</details>

16. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -
OpenAI Codex v0.117.0 (research preview)
--------
workdir: /Users/jleechan/projects/jlee...

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR Current State ==="
gh pr view 539 --repo jleechanorg/jleechanclaw --json sta...

18. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR Current State ==="
gh pr view 539 --repo jleechanorg/jleechanclaw --json sta...

19. @coderabbitai all good?

20. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR Current State ==="
gh pr view 539 --repo jleechanorg/jleechanclaw --json sta...

21. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

22. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -
OpenAI Codex v0.117.0 (research preview)
--------
workdir: /Users/jleechan/projects/jlee...

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR Current State ==="
gh pr view 539 --repo jleechanorg/jleechanclaw --json sta...

24. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR Current State ==="
gh pr view 539 --repo jleechanorg/jleechanclaw --json sta...

25. **VERDICT: PASS** — skeptic-cron evaluated and merged this PR. All 6 criteria confirmed green.  \n\n<!-- HEAD-SHA: e53b9acaad7b7e19949a1d1fea86fb2e32213786 -->

