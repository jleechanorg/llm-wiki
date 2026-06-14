---
title: "PR 5 routing migration rebased onto PR 5.5"
type: source
tags: [level-up, routing-migration, rebase, pr-7377, worldarchitect-ai]
date: 2026-06-08
source_file: raw/project_2026-06-08_pr5_routing_migration_rebased.md
---

## Summary
PR #7377 rebased onto PR 5.5 head e5a5d5a0b1 per new chain order PR 1→2→3→4→5.5→5→6. Old SHA 057e453435 → new SHA ecf279618b (force-with-lease per user approval). 992 passed, 12 skipped, 130 subtests passed in 5.54s. 6 switch points in mvp_site/agents.py route from canonical level_up_session.status; 5 read-side routing adapters in level_up_session.py. Lessons: gh pr edit --base works to retarget an open PR's base branch without close+reopen; 0 file overlap between PR 5 and PR 5.5 (PR 5.5 added canonical_signal gate, PR 5 added read-side adapters on different lines).

## Key Claims
- Rebase after push requires force-with-lease — ASK first. Old directive's 'first push to new remote, NOT a force-push' was ambiguous; user approved --force-with-lease once conflict was named explicitly
- 0 file overlap between PR 5 and PR 5.5 (git diff --name-only + comm -12); rebase was a clean fast-forward replay of one commit
- PR 5.5 also modified level_up_session.py (commit 55782df35b added canonical_signal gate); PR 5 also modified it (added read-side adapters); no conflict because different lines
- gh pr edit --base <new-base> works to retarget an open PR's base branch without needing to close and reopen
- 7-file pytest directive catches all 6 switch points + routing-adapter API surface in one run

## Connections
- [[project_2026-06-08_level_up_session_state_machine_pivot]]
- [[LevelUpRoutingMigration]]
- [[GitBaseRetarget]]
