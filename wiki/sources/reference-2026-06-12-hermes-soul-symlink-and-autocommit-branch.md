---
title: "Hermes SOUL.md symlink + auto/commit-pending branch hygiene (2026-06-12)"
type: source
tags: [hermes, soul-md, symlink, autocommit-branch, integrate, content-diff, working-tree, deploy-sh]
date: 2026-06-12
source_file: raw/reference_2026-06-12_hermes_soul_symlink_and_autocommit_branch.md
---

## Summary
Two non-obvious facts about `~/.hermes` discovered during a `/integrate` on 2026-06-12: (1) root `SOUL.md` is a SYMLINK to `workspace/SOUL.md` — grep and git disagree on whether "SOUL.md changed" (grep follows symlink, git treats the symlink blob as unchanging); (2) `auto/commit-pending` is an automation branch that can carry a stale working-tree snapshot (the live working tree can be behind origin/main), and on 2026-06-12 its `scripts/deploy.sh` was the OLD buggy `PROD_PORT=8643` version that would have UNDONE the just-merged #611 fix had it reached main.

## Key Claims
- `git show <ref>:SOUL.md` prints the literal text `workspace/SOUL.md` (the symlink blob), NOT the policy content
- `git log -S '<text>' -- SOUL.md` finds NOTHING for content changes — the symlink blob never changes; search `-- workspace/SOUL.md` instead
- `grep '<text>' SOUL.md` DOES match (grep follows the symlink) — grep and git disagree
- SOUL personalization commits land in `workspace/SOUL.md`; to preserve/cherry-pick a SOUL rule, target `workspace/SOUL.md`
- `auto/commit-pending` snapshots whatever is dirty in the live working tree — can be **behind origin/main**
- Before forcing `auto/commit-pending` forward, content-diff each commit vs origin/main (`git diff origin/main -- <file>`); don't trust commit messages or the squash-merge detector (it matches by message and misses content-identical-but-renamed cases)
- `integrate.sh --force` switches to local `main`, merges origin/main (force-resolves divergence), then creates a fresh `dev<ts>` branch; does NOT delete branches with unmerged commits, so `auto/commit-pending` stays recoverable for cherry-pick

## Key Quotes
> "On 2026-06-12 its `scripts/deploy.sh` was the OLD buggy `PROD_PORT=8643` version (and it deleted `tests/test_deploy_port_defaults.py`) — i.e. those local commits would have **UNDONE** the just-merged #611 fix had they reached main."

> "Don't trust commit messages or the squash-merge detector (it matches by message and misses content-identical-but-renamed cases). Drop commits that revert merged work; cherry-pick only genuinely-new content."

## Connections
- [[HermesSOULSymlink]] — root symlink → workspace/SOUL.md
- [[AutoCommitPendingBranch]] — stale working-tree snapshot risk
- [[IntegrateRecipe]] — safe integrate.sh --force pattern
- [[SquashMergeDivergence]] — content-diff vs SHA ancestry
- [[HermesGateway]] — ~/.hermes vs ~/.hermes_prod
