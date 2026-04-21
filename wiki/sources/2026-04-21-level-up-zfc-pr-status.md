---
title: "ZFC Level-Up PR Status — 2026-04-21"
type: source
tags: [level-up, zfc, pr-status, roadmap]
date: 2026-04-21
source_file: ~/llm_wiki/raw/2026-04-21-level-up-zfc-pr-status.md
---

## Summary

PR queue snapshot for the ZFC Level-Up project as of 2026-04-21. Two PRs are merge-ready (#6423, #6422). PR #6420 (Stage 0 cleanup) is the active lane — CR CHANGES_REQUESTED, with harness contract hash mismatch from a schema change. PR #6418 is officially parked/superseded per roadmap decision. PR #6404 (architecture lane) has CR APPROVED but may have stale harness autonomy failures.

## Key Claims

- PR #6423 (`fix/node24-workflow-deprecation`) — CR APPROVED, merge-ready, no blockers
- PR #6422 (`fix/beads-history-main`) — CR APPROVED, merge-ready, no blockers
- PR #6420 (`fix/zfc-level-up-m0-v4`) — Stage 0 ZFC cleanup; CI ✅, CR CHANGES_REQUESTED; harness contract hash mismatch triggered by `new_level` schema addition to RewardsBox TypedDict
- PR #6404 (`feat/zfc-level-up-model-computes`) — CR APPROVED; harness autonomy may be stale failure
- PR #6418 (`test/level-up-enforcement-clean`) — Superseded per roadmap; should not continue as written

## Key Learnings (2026-04-21)

- Git identity worktree-local config (`.git/worktrees/<name>/config`) silently overrides global `~/.gitconfig` — commits appear under wrong author with no warning
- Generic deletion-milestone skill created at `~/.claude/skills/deletion-milestone.md` (applies to ANY project)
- Three key deletion-milestone learnings: (1) CI gates proposed in RCA but never built — fix requires explicit bead deliverables; (2) generic vs project-specific skill split; (3) anti-substitution for deletion milestones — net LOC ≤ 0 non-negotiable

## Connections

- [[Level-Up ZFC Architecture]] — model computes level-up signal, backend formats
- [[Deletion Milestone Discipline]] — generic skill for deletion/quarantine work
- [[PR #6420]] — active Stage 0 lane
- [[PR #6404]] — architecture lane, post-M0
- [[PR #6418]] — parked/superseded
