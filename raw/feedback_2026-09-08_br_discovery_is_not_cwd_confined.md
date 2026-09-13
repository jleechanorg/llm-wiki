---
name: br-discovery-is-not-cwd-confined
description: "br binds to another checkout's beads.db when a worktree has no local one, so mutations land silently on the wrong branch"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: facf2bde-3f32-4d25-a7bb-1c6179b04f81
  modified: 2026-09-13T16:17:53.881Z
---

`br`'s database discovery walks outward from the cwd. In a worktree with no local
`.beads/beads.db`, it can bind to a **different checkout's** database — `br update`
then succeeds, writes to that other branch, and leaves your own worktree with no
diff and no error.

2026-09-08: a delegated lane ran 83 `br update` calls from a fresh worktree; every
one landed in `~/projects_other/jleechan-skills` on an unrelated branch. Nothing
failed. It was caught only because the lane ran `br info` on its own initiative
before pushing, then `git restore`d the other checkout and redid the work.

**Why:** the failure is silent and invisible from the worktree you are in — the
usual "did it work?" check (`git status` / `git diff` locally) shows clean, which
reads as "no changes needed" rather than "changes went elsewhere." Running many
worktrees of one repo concurrently makes this the default hazard, not an edge case.

**How to apply:** before the first `br` *mutation* in any worktree — not just before
diagnosis — run `br where`/`br info` and confirm the resolved path is under this
worktree. If there is no local database, build one from the worktree's own JSONL
with `br sync --import-only`, then pin every mutating call:
`br --db "$(pwd)/.beads/beads.db" update ...`. Written into
`~/.claude/skills/beads-issue-tracking/SKILL.md` § Worktrees and conflicts.

Related: [[worktree-beads-lost-in-reconciliation]], [[bead-vanished-concurrent-writer-collision]],
[[integrate-shared-worktree-concurrent-session-collision]], [[shared-checkout-git-reads-are-racy]]

**2026-09-13 addendum — shadowing happens even with a local DB present.** During
PR #9842's review, plain `br show`/`br close` in `worktree_startup_probe`
intermittently returned "Issue not found" for beads (`rev-3mj69`, `rev-rmwt8`)
that did exist — even though this worktree had its own valid
`.beads/beads.db` and `.beads/config.yaml`. `br config path` revealed why: a
**"Project config"** entry resolved to the *main checkout's*
`/Users/jleechan/projects/worldarchitect.ai/.beads/config.yaml`, a different
physical file (confirmed by differing inodes) from the worktree's local one.
Default discovery isn't just "walk outward and find nothing local, so fall
back" — a registered project config can outrank a present, valid local one.
`br --db .beads/beads.db <cmd>` (explicit relative path) reliably targets the
worktree's own database; plain `br` does not. Treat "a local `.beads/` exists"
as insufficient — pin `--db` unconditionally, every command, in every
worktree that isn't the primary checkout. Bead:
`rev-learning-br-project-registry-shadows-local-db-o1agl`.
