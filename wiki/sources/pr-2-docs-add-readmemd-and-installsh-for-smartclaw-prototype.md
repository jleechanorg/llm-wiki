---
title: "docs: add README.md and install.sh for SmartClaw prototype"
type: source
tags: [github, pr, jleechanorg-smartclaw]
sources: []
date: 2026-03-29
pr_url: https://github.com/jleechanorg/smartclaw/pull/2
pr_number: 2
pr_repo: jleechanorg/smartclaw
---

## Summary
## Summary
- Add comprehensive README.md with WIP prototype disclaimer
- Differentiate SmartClaw from Agent-Orchestrator (jleechanclaw)
- Add install.sh with prerequisite checking and environment setup
- Add .env.example for safe configuration (never commit secrets)

## Background
SmartClaw is a prototype reference repo for the OpenClaw autonomous orchestrator. This establishes the initial documentation and installation scripts.

## Test plan
- [ ] Verify README.md renders correctly
- [ ] Verify...

## Key Changes
- 5 commit(s) in this PR
- 0 file(s) changed

- Merged: 2026-03-29

## Commit Messages
1. docs: add README.md and install.sh for SmartClaw prototype
  
  - Add comprehensive README with WIP disclaimer
  - Differentiate SmartClaw from Agent-Orchestrator
  - Add install.sh with prerequisite checking
  - Add .env.example for safe configuration
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
2. fix: replace real Slack IDs with placeholder values
  
  Replace actual Slack user/channel IDs with placeholder format
  (U0000000000, C0000000000, D0000000000) in .env.example and README.md.
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
3. Fix hardcoded absolute path in .claude/settings.json
  
  Replace user-specific absolute path with relative path to make the settings file portable across different environments
4. feat: add .coderabbit.yaml with request_changes_workflow enabled
  
  Enables CodeRabbit to post formal APPROVED/CHANGES_REQUESTED reviews.
  Required for 7-green Gate 3 criteria.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. Merge remote-tracking branch 'origin/main' into docs/smartclaw-readme

## Files Changed

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **2...

2. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 2 --repo jleechanorg/smartclaw --json state,mergeable...

4. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 2 --repo jleechanorg/smartclaw --json state,mergeable...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me check the current state of the PR before answering.

---

🏁 Script executed:
```
#!/bin/bash
echo "=== LATEST COMMITS...

8. @coderabbitai review

9. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

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
echo "=== LATEST COMMITS ==="
gh api repos/jleechanorg/smartclaw/pulls/2/commits --jq '.[...

12. @coderabbitai all good?

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== LATEST COMMITS ==="
gh api repos/jleechanorg/smartclaw/pulls/2/commits --jq '.[...

