---
title: "Extract automation bug fixes from PR #5584 into dedicated PR"
type: source
tags: ["task", "p2", "bead"]
bead_id: "jleechan-9ga9"
priority: P2
issue_type: task
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [task]** Extract automation bug fixes from PR #5584 into dedicated PR

## Details
- **Bead ID:** `jleechan-9ga9`
- **Priority:** P2
- **Type:** task
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

PR #5584 (Schema Prompt Drift Fixes) contains unrelated automation bug fixes that were committed directly on the `schema_followup` branch. These should be cherry-picked to their own branch and merged independently.

## Unrelated files in PR #5584

**Automation (directly committed on branch, no parent PR#):**
- `automation/jleechanorg_pr_automation/jleechanorg_pr_monitor.py` — Boolean mergeable detection fix (commits: abd562d76, 1aa6990d8)
- `automation/.../tests/test_fixpr_return_value.py` — GitHub API mock format correction (commit: d72c13f67)
- `automation/.../tests/test_mergeable_conflict_detection.py` — NEW test file added to cover the fix

**Meta/docs churn (borderline — accumulated on long-running branch):**
- `CLAUDE.md` — 4 CLAUDE.md edits (expand/condense/revert/expand)
- `AGENTS.md` + `.claude/skills/end2end-testing.md` + `.claude/skills/testing-infrastructure.md`

## Action
1. After PR #5584 merges, create a new branch from main
2. Cherry-pick the 3 automation commits (abd562d76, d72c13f67, 1aa6990d8)
3. Open a PR titled "fix(automation): correct merge conflict detection for Boolean mergeable API response"
4. The CLAUDE.md/AGENTS.md churn can stay in #5584 (low risk, already reviewed)

