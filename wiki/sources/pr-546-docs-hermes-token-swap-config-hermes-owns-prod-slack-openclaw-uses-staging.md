---
title: "docs: Hermes token-swap config — Hermes owns prod Slack, OpenClaw uses staging"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-11
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/546
pr_number: 546
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary

Token swap (2026-04-11) to enable simultaneous Hermes + OpenClaw operation:

- **Hermes** `~/.hermes/.env`: `SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN` set to **prod** Slack app tokens
- **OpenClaw prod** `~/.openclaw_prod/openclaw.json`: `channels.slack` updated to **staging** Slack app tokens
- `GATEWAY_ALLOW_ALL_USERS=true` added to hermes `.env` (required for DM access)

Both gateways now run simultaneously on **different Slack apps** — no event conflicts.

Hermes owns the **prod Slack...

## Key Changes
- 10 commit(s) in this PR
- 2 file(s) changed

- Merged: 2026-04-11

## Commit Messages
1. docs: add SWITCH_TO_HERMES guide
  
  Document using Hermes Agent as primary AI with OpenClaw AO
  automation preserved. Covers gateway comparison, simultaneous
  operation (different Slack apps), quick-start, and troubleshooting.
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
2. docs: update SWITCH_TO_HERMES with token-swap config
  
  Token swap (2026-04-11):
  - Hermes: SLACK_BOT_TOKEN + SLACK_APP_TOKEN = prod app (xoxb-...L1ZG...)
  - OpenClaw prod gateway: channels.slack = staging app (xoxb-...roQR...)
  - GATEWAY_ALLOW_ALL_USERS=true in hermes .env
  Both gateways now run simultaneously on different Slack apps.
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
3. security: redact live Slack API tokens from documentation
  
  Replace exposed xoxb- and xapp- tokens with redacted placeholders
  to prevent credential leakage in git history.
4. fix: add HTML scaffolding, fix mermaid double-braces, soften event-conflicts claim
5. merge: resolve conflicts taking branch version of SWITCH_TO_HERMES docs
6. fix: remove duplicate section/h2 IDs causing invalid HTML
7. fix: neutralize token fragments, add scroll-margin to h2 elements
8. fix: use rg -q to avoid printing Slack token values in troubleshooting
9. ci: retrigger CodeRabbit review
10. docs: remove unused mermaid CDN from SWITCH_TO_HERMES.html
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

## Files Changed
- `docs/SWITCH_TO_HERMES.html`
- `docs/SWITCH_TO_HERMES.md`

## Review Notes
1. You have reached your Codex usage limits for code reviews. You can see your limits in the [Codex usage dashboard](https://chatgpt.com/codex/cloud/settings/usage).
To continue using code reviews, add credits to your account and enable them for code reviews in your [settings](https://chatgpt.com/codex...

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: review paused by coderabbit.ai -->

> [!NOTE]
> ## Reviews paused
> 
> It looks like this branch is under active development. To avoid overwhelming you with review comments due to an influx...

3. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -. Claude: Command failed: /Users/jleechan/.local/bin/claude --dangerously-skip-permissions --print --model claude-sonnet-4-6.


_Pos...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

8. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -. Claude: Command failed: /Users/jleechan/.local/bin/claude --dangerously-skip-permissions --print --model claude-sonnet-4-6.


_Pos...

9. @coderabbitai all good?

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

11. @coderabbitai all good?

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

13. @coderabbitai all good?

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

15. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -. Claude: Command failed: /Users/jleechan/.local/bin/claude --dangerously-skip-permissions --print --model claude-sonnet-4-6.


_Pos...

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
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

19. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

20. @coderabbitai all good?

21. @coderabbitai all good?

22. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

24. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -. Claude: Command failed: /Users/jleechan/.local/bin/claude --dangerously-skip-permissions --print --model claude-sonnet-4-6.


_Pos...

25. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

26. @coderabbitai all good?

27. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

28. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

29. @coderabbitai all good?

30. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

31. @coderabbitai please re-review

32. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,headRefName,commits -q '{state: .state, mergeable: ...

33. @coderabbitai all good?

34. @coderabbitai all good?

35. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

36. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 546 --repo jleechanorg/jleechanclaw --json state,merg...

37. ## Green Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=3 |
| 2. No conflicts | PASS | mergeable=true, state=unstable |
| 3. CR approved | PASS | state=APPROVED...

38. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -. Claude: Command failed: /Users/jleechan/.local/bin/claude --dangerously-skip-permissions --print --model claude-sonnet-4-6.


_Pos...

