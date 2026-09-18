---
title: "Squash-merge AUTHORITY doclint trap"
type: concept
tags: [git, squash-merge, doclint, worldai_claw]
sources: [feedback-2026-09-17-sprite-builder-swarm-five-traps, pr320-merged-spec-on-main]
last_updated: 2026-09-17
---

In worldai_claw, `docs/plans/worldai-2d/contracts/AUTHORITY.md` records, per governed doc, the latest commit SHA that touched it; `packages/game-contracts/test/doclint/authority.test.ts` fails closed when the recorded SHA is not `git log -1 -- <path>`. A **squash merge** mints a new SHA for the docs, so the table on main immediately points at a commit that no longer touched the path. Seen 2026-07-28 (PR #320) and again 2026-09-17 (PR #434 → main 5a903f80), where it cascaded to every PR that merged main.

**Recovery:** refresh the `this repo` rows to `git log -1 --format=%H -- <path>` at the base of the stacked PRs and merge upward. **Prevention (open follow-up, bead wc-yxptc):** branch protection requiring merge commits, or a doclint job on pushes to main.

Related: [[feedback-2026-09-17-sprite-builder-swarm-five-traps]], [[GitWorkflow]].
