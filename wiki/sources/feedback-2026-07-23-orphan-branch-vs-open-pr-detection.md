---
title: "Orphan branch detection: cross-reference local ahead-of-main with gh pr list"
type: source
tags: [feedback, git-workflow, pr-management, llm-inspector]
date: 2026-07-23
source_file: feedback_2026-07-23_orphan-branch-vs-open-pr-detection.md
---

## Summary

Pre-merge protocol for catching orphaned local branches before they create duplicate or divergent work on main. When a local branch and an open PR share a feature name, the PR (typically from claude/sonnet) is usually the canonical one to merge — the local branch is orphan. Verified on llm-inspector PR #15 vs local `feat/skills-usage-tracking` (divergent 8000+ LOC).

## Key Claims

- Always cross-reference `git branch` (ahead of origin/main) with `gh pr list --state all --json headRefName` before merging
- If a local branch and an open PR share a feature name, the PR is canonical; the local is orphan
- Decision matrix: 4 local-vs-PR states → action (drop, merge-only, push-as-new-PR, push+create-PR)
- Do NOT auto-delete orphan branches — destructive action stays user-gated per global CLAUDE.md

## Key Quotes

> When scanning local branches for work to merge, **always cross-reference with `gh pr list --state all --json headRefName`** before deciding what to merge.

> **Merge-only-the-PR pattern**: when local is orphan, do NOT push it, do NOT create a competing PR. Squash-merge the live PR with `--delete-branch`. Mention the orphan in the final report so the user can `git branch -D` it explicitly (destructive action stays user-gated).

## Connections

- [[LLMInspector]] — verified on this repo; PR #15 (claude/sonnet) superseded local feat/skills-usage-tracking (jleechan2015)
- [[IntegrateCommand]] — same session: /integrate to dev1784850819 after the merges
- [[CodexSonnetBranchingPattern]] — claude/sonnet frequently creates its own branches with -flag/-support suffixes; same-named local branches should always be cross-referenced first
- [[MergeSafetyPolicy]] — non-worldarchitect.ai repos use "standard caution (CI green + review + no conflicts)"; user-explicit merge instructions are sufficient when CodeRabbit rate-limits

## Decision Matrix

| Local branch state | Open PR state | Action |
|---|---|---|
| Local is fast-forward of merged PR | Either | `git branch -D local` (no-op since same commits) |
| Local diverges from open PR | PR MERGEABLE | Merge PR, flag local as orphan for deletion |
| Local diverges from open PR | PR closed/not-mergeable | Push local as new PR, close stale PR |
| Local only (no PR) | None | Push branch + `gh pr create` |

## Provenance

- Session: 2026-07-23, branch `feat/codex-e2e-support`
- Source: `~/.claude/projects/-Users-jleechan-projects-other-llm-inspector/memory/feedback_2026-07-23_orphan-branch-vs-open-pr-detection.md`
- Incident: local `feat/skills-usage-tracking` (commit 0520f3c by jleechan2015) vs PR #15 `feat/skills-usage-flag` (commit 2db62f6 by claude/sonnet) — both targeting `--skills-usage` flag but divergent 8000+ LOC