---
name: project_2026-06-08_level_up_reducer_diverged_across_chain
description: "level_up_session.py reducer has diverged into 4 different versions across the PR1-PR5.5 chain (none merged to main) — converges only via rebase onto consolidated PR1, which is force-push/merge-gated"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9155598c-34bd-4af3-988c-94b2dc925fb7
---

The canonical level-up reducer `mvp_site/level_up_session.py` is **ABSENT on origin/main** (PR1 #7368 not merged) and has **diverged into 4 distinct versions** across the migration chain because the downstream branches were created BEFORE today's (2026-06-08) PR1 consolidation (commit 954b88557f), so each carries its own older reducer copy rather than PR1's canonical content as a subset:

- **PR1 #7368** (`feature/level-up-session-reducer`): canonical, blob `426e316a2352`, **831 lines** — the source of truth, smallest, consolidated last
- **PR4 #7376** / **PR5.5 #7374**: shared blob `3dc6e2dbda80`, **891 lines** (+60 over PR1; PR5.5 branched from/shares PR4's reducer base — scope bleed for an "observability-only" PR)
- **PR2 #7369**: blob `f9a4ba0939de`, **904 lines** (PR1 base + 3 reducer guards from commit 1e4dc0c8e3: begin_finish_commit story_id-None guard, complete_finish_commit last_error pop, mark_finish_error TERMINAL_STATUSES guard)
- **PR3 #7370**: blob `b529244cb84c`, **929 lines** (most changes)

**Why:** Per-PR review/CI is UNAFFECTED — each branch is internally consistent. Only clean sequential **merge** is blocked: at merge time each branch modified the reducer differently from the common ancestor → guaranteed conflicts.

**How to apply:** The clean resolution = merge PR1 first, then rebase each downstream PR onto the new main (PR1→PR2→PR3→PR4→PR5.5 order) resolving the reducer to canonical+own-delta. This requires **force-pushes (human-gated) and merge authority (human-gated)** — I cannot collapse the divergence autonomously under the no-force-push / no-merge constraints. Surface as a cross-PR integration finding requiring a human decision on merge strategy; do NOT delete/modify any branch's reducer to chase a gate (e.g. #7374 Skeptic Gate 8d flags the 891-line reducer as an out-of-scope "new file" — that is a consequence of PR1 being unmerged, documented as a Known Limitation, not a true scope violation). Related: [[project_2026-06-09_pr7366_supersedes_pr1_conflict]], [[project_2026-06-08_level_up_session_pr1to3_shipped]], [[project_2026-06-08_level_up_session_state_machine_pivot]].
