---
title: "Level-up reducer diverged into 4 versions across PR1–PR5.5 chain"
type: source
tags: [level-up, reducer, pr-chain, merge-conflict, worldarchitect-ai, state-machine]
date: 2026-06-08
source_file: raw/project_2026-06-08_level_up_reducer_diverged_across_chain.md
---

## Summary
The canonical level-up reducer mvp_site/level_up_session.py is ABSENT on origin/main (PR1 #7368 not merged) and has diverged into 4 distinct versions across the migration chain (PR1 831 lines, PR2 904, PR3 929, PR4/PR5.5 891). Each downstream branch carries its own older reducer copy. Per-PR review/CI is UNAFFECTED (each branch internally consistent), but clean sequential merge is blocked. Clean resolution = merge PR1 first then rebase downstream — requires force-pushes and merge authority, both human-gated.

## Key Claims
- 4 distinct reducer blobs across the chain: PR1 #7368 (426e316a, 831 lines canonical), PR4 #7376/PR5.5 #7374 (3dc6e2db, 891 lines), PR2 #7369 (f9a4ba09, 904 lines), PR3 #7370 (b529244c, 929 lines)
- Each downstream branch was created BEFORE PR1's 2026-06-08 consolidation commit 954b88557f, so they carry older reducer copies
- Per-PR review/CI passes (each branch internally consistent); only sequential merge is blocked
- Resolution = merge PR1 first then rebase each downstream PR (PR1→PR2→PR3→PR4→PR5.5 order); requires force-pushes (human-gated) and merge authority (human-gated)
- Skeptic Gate 8d flags the 891-line reducer as 'new file' scope violation on #7374 — that is a consequence of PR1 being unmerged, not a true scope violation

## Connections
- [[project_2026-06-09_pr7366_supersedes_pr1_conflict]]
- [[project_2026-06-08_level_up_session_pr1to3_shipped]]
- [[project_2026-06-08_level_up_session_state_machine_pivot]]
- [[LevelUpReducer]]
