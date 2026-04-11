---
title: "docs: add OpenClaw context-window ASCII diagram"
type: source
tags: [github, pr, jleechanorg-smartclaw]
sources: []
date: 2026-03-30
pr_url: https://github.com/jleechanorg/smartclaw/pull/5
pr_number: 5
pr_repo: jleechanorg/smartclaw
---

## Summary
## Summary\n- add a new markdown doc with an OpenClaw-vs-AO ASCII context-window comparison\n- replace the original Zoe/Codex framing with Jeffrey's real OpenClaw stack\n- include system-relevant elements: SOUL/AGENTS/TOOLS, memory files, launchd/cron, AO dispatch, and merge-gate targets\n\n## File\n- docs/OPENCLAW_CONTEXT_WINDOW_COMPARISON.md\n\n## Notes\n- this is documentation-only (no runtime behavior changes)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Documentation-only change...

## Key Changes
- 4 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-03-30

## Commit Messages
1. docs: add OpenClaw context-window ASCII comparison
2. docs: reframe OpenClaw diagram with business focus
3. fix: pluralize 'AO WORKER RISK ZONES' → 'AO WORKERS RISK ZONES' per CodeRabbit review
4. chore: retrigger CodeRabbit re-review

## Files Changed
- `docs/OPENCLAW_CONTEXT_WINDOW_COMPARISON.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- walkthrough_start -->

<details>
<summary>📝 Walkthrough</summary>

## Walkthrough

A new documentation file adds a side-by-side context-window comparison of OPENCLAW (Business Orchestrator) and AO WORKERS (Execution Agents),...

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check PR status and open review comments
gh pr view 5 --repo jleechanorg/smartclaw --js...

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
# Get PR details including mergeable state, CI checks, and reviews
gh pr view 5 --repo jl...

6. @coderabbitai all good?

7. Pushed fix for the singular/plural heading. Please re-review. Thanks!

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 5 --repo jleechanorg/smartclaw --json state,mergeable,mergeStateStatus,reviewD...

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
echo "=== PR STATE ==="
gh pr view 5 --repo jleechanorg/smartclaw --json state,mergeable,...

11. @coderabbitai all good?

12. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] Yes, all good! ✅

Based on the review at commit `df6ee2c9`:

- **CI Checks:** 3/3 passing
- **Merge Status:** Clean, no conflicts
- **Review Decisio...

