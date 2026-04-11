---
title: "refactor(claw): replace Python task-classifier with LLM judgment"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-05
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/502
pr_number: 502
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary

- Remove Python inline script for task classification (coding vs read_only)
- Remove Python inline script for ISSUE_ID extraction from task description
- Replace both with LLM judgment (the LLM already has full context)
- Reduces shell complexity and removes fragile regex matching

## Test plan

- [ ] Verify /claw still correctly classifies a coding task (e.g. "fix orch-sq2")
- [ ] Verify /claw still correctly classifies a read-only task (e.g. "what time is it")
- [ ] Verify ISSUE_ID...

## Key Changes
- 2 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-05

## Commit Messages
1. refactor(claw): replace Python task-classifier with LLM judgment
  
  Remove the Python inline script that used regex keyword matching to
  classify tasks as coding vs read_only. The LLM already has full context
  and can make this judgment more accurately. Same approach for ISSUE_ID
  extraction — let the LLM read and identify bead IDs rather than brittle
  regex matching.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
2. fix(claw): replace regexp/python3 classification with LLM judgment
  
  - is_coding_task(): remove 20-pattern python3 regex; LLM classifies directly
  - ISSUE_ID extraction: remove python3 re.search; LLM scans task naturally
  - RUNTIME_FLAG detection: remove python3 antig regex; LLM judges directly
  - HAS_LEARN gate: replace python3 regex with fail-closed LLM judgment
  - Session fallback: remove dangerous tail -1 (wrong session in parallel mode)
  
  LLM judgment is more robust than brittle regex for intent classification.
  Fail-closed HAS_LEARN: always append /learn unless explicitly present.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `.claude/commands/claw.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- walkthrough_start -->

<details>
<summary>📝 Walkthrough</summary>

## Walkthrough

A command script was refactored to remove automated pattern-matching logic and subprocess-based detection, replacing it with manual placehold...

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
`@github-actions`[bot]: I'm replying to the latest comment without visibility into the earlier conversation (it's too long to be included in my context).

Based on the PR objectives alone, here's a quick status check:

**Key concern (still open)...

4. @codex @coderabbitai @cursor @copilot [AI automation] Codex will implement the code updates while coderabbitai, cursor, and copilot focus on review support. Please make the following changes to this PR.

**Summary (Execution Flow):**
1. Review every outstanding PR comment to understand required fixe...

5. To use Codex here, [create an environment for this repo](https://chatgpt.com/codex/settings/environments).

6. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | FAIL | state=CHAN...

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fetch all PR review comments
gh pr view 502 --repo jleechanorg/jleechanclaw --json revi...

