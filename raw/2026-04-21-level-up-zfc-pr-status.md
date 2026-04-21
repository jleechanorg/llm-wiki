# ZFC Level-Up PR Status Snapshot — 2026-04-21

## PR Queue (as of 2026-04-21 ~01:45 America/Los_Angeles)

### Ready to Merge (CR APPROVED, MERGEABLE)
- **PR #6423** — `fix/node24-workflow-deprecation` — Node.js 24 opt-in for self-hosted shard
- **PR #6422** — `fix/beads-history-main` — restore missing related PR review tasks

### Active Lanes — Blockers Present
- **PR #6420** — `fix/zfc-level-up-m0-v4` — Stage 0 ZFC level-up cleanup
  - State: OPEN, MERGEABLE ✅
  - CI: ✅ SUCCESS
  - CR: CHANGES_REQUESTED (coderabbitai @ 2026-04-21)
  - Blocker: schema `new_level` in RewardsBox TypedDict + harness contract hash mismatch
  - Commits: `d4684dee8` (schema fix), `d9c48d9cc` (dead-code fix)

- **PR #6404** — `feat/zfc-level-up-model-computes` — Model-owned signal formatter
  - State: OPEN, MERGEABLE ✅
  - CR: APPROVED (coderabbitai @ 2026-04-21)
  - Harness autonomy check: may be stale (pre-existing failure)

### Parked / Superseded
- **PR #6418** — `test/level-up-enforcement-clean` — Superseded per roadmap decision
  - CR: CHANGES_REQUESTED (oscillating APPROVED/CHANGES_REQUESTED)
  - Should not continue as written; narrow enforcement PR to follow #6420

## Key Learnings (2026-04-21)
- Git identity worktree-local config silently overrides global → commits under "jleechan" not "jleechan2015"
- Generic deletion-milestone skill created at `~/.claude/skills/deletion-milestone.md`
- Three key learnings: (1) CI gates proposed in RCA but never built, (2) generic vs project-specific skill split, (3) anti-substitution for deletion milestones

## Next Up
1. Land #6423 + #6422 (merge-ready, no blockers)
2. Fix #6420 harness contract hash (schema change triggered mismatch)
3. After #6420 lands → narrow enforcement PR for #6418 cleanup
