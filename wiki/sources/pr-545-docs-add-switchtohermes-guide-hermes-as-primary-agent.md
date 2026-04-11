---
title: "docs: add SWITCH_TO_HERMES guide — Hermes as primary agent"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-11
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/545
pr_number: 545
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary

- Add `docs/SWITCH_TO_HERMES.md` (and `.html`) explaining how to use Hermes Agent as the primary AI while preserving OpenClaw for AO automation
- Hermes runs its own gateway connected to the `hermes-slack` Slack app
- OpenClaw gateway stays up for AO automation (skeptic-cron, merge gates, PR reactions)
- Both gateways can run simultaneously since they use different Slack apps/tokens

## Test plan

- [x] `hermes status` shows gateway running
- [x] `curl http://127.0.0.1:18789/health`...

## Key Changes
- 4 commit(s) in this PR
- 2 file(s) changed

- Merged: 2026-04-11

## Commit Messages
1. docs: add SWITCH_TO_HERMES guide
  
  Document using Hermes Agent as primary AI with OpenClaw AO
  automation preserved. Covers gateway comparison, simultaneous
  operation (different Slack apps), quick-start, and troubleshooting.
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
2. fix: resolve CodeRabbit review comments on SWITCH_TO_HERMES docs
  
  - Add sidebar nav with scroll-spy (IntersectionObserver) and heading id anchors
  - Remove hardcoded "1038 commits behind" staleness from hermes update instruction
  - Change /health to /mcp/health (2 occurrences in MD, 2 in HTML) to match
    human_channel_bridge.py check_mcp_mail_health() endpoint
  - Remove unused mermaid.js CDN and init call (Bugbot low-severity finding)
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
3. fix: add missing body styles to SWITCH_TO_HERMES.html
  
  Adds the missing body rule with dark background, text color, font family,
  font size, and line height to match other HTML docs in docs/ directory.
  Without these styles, the page rendered light text on white background,
  making it unreadable.
4. fix: add missing body styles and fix scroll-spy observer (Bugbot)
  
  - Add body{background,color,font-family,font-size,line-height} so dark theme
    renders correctly (Bugbot high-severity finding)
  - Remove h3[id] from IntersectionObserver selector — h3 subsections have no
    sidebar links, so scrolling past them was clearing the active highlight
    without restoring it (Bugbot low-severity finding)
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

## Files Changed
- `docs/SWITCH_TO_HERMES.html`
- `docs/SWITCH_TO_HERMES.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
No actionable comments were generated in the recent review. 🎉

<details>
<summary>ℹ️ Recent review info</summary>

<details>
<summary>⚙️ Run configuration</summary>

**Configuration used**: Path: .coderabbit.yaml

**Review profil...

2. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #545: docs: add SWITCH_TO_HERMES guide — Adds `.md` and `.html` documentation files explaining Hermes Agent as a primary AI agent while preserving OpenClaw for AO automati...

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get coderabbitai's review comments on PR `#545`
gh pr view 545 --repo jleechanorg/jleec...

4. @coderabbitai all good?

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check all commits on the PR branch
gh api repos/jleechanorg/jleechanclaw/pulls/545/comm...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Yes, all good from my side! ✅ The second commit (`f05837b4`) resolved all 4 of my previously flagged issues (sidebar nav + scroll-spy, stale "commits beh...

8. @coderabbitai all good?

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] — Yes, all good from my side! ✅

All 4 of my previously flagged issues are confirmed resolved in the second commit (`f05837b4`):

| # | Issue | Stat...

10. @coderabbitai all good?

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] — Yes, all good from my side! ✅

All 4 of my previously flagged issues are confirmed resolved in the second commit (`f05837b4`):

| # | Issue | Stat...

12. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec --model gpt-5.4 -. Claude: Command failed: /Users/jleechan/.local/bin/claude --dangerously-skip-permissions --print --model claude-sonnet-4-6.


_Pos...

13. ## Green Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=3 |
| 2. No conflicts | PASS | mergeable=true, state=unstable |
| 3. CR approved | PASS | state=APPROVED...

