---
name: hermes-soul-symlink-and-autocommit-branch-hygiene
description: Root ~/.hermes/SOUL.md is a symlink to workspace/SOUL.md; the auto/commit-pending branch can hold a stale working-tree snapshot that would undo merged fixes
metadata: 
  node_type: memory
  type: reference
  originSessionId: c594d4f0-a942-4271-85f6-5407a3c1d6e6
---

Two non-obvious facts about `~/.hermes` discovered during a `/integrate` on 2026-06-12.

## 1. Root SOUL.md is a SYMLINK → workspace/SOUL.md

`~/.hermes/SOUL.md` (the gateway-read policy file) is a **symlink** whose target is `workspace/SOUL.md` (the real 27 KB file). Consequences:
- `git show <ref>:SOUL.md` prints the literal text `workspace/SOUL.md` (the symlink blob), NOT the policy content.
- `git log -S '<text>' -- SOUL.md` finds NOTHING for content changes — the symlink blob never changes. Search `-- workspace/SOUL.md` instead.
- `grep '<text>' SOUL.md` DOES match (grep follows the symlink). So grep and git disagree on whether "SOUL.md changed".
- SOUL personalization commits (e.g. COMMIT trigger-rule mappings) land in `workspace/SOUL.md`. To preserve/cherry-pick a SOUL rule, target `workspace/SOUL.md`.

## 2. `auto/commit-pending` is an automation branch that can carry STALE content

`~/.hermes` is often parked on a branch named **`auto/commit-pending`** created by an auto-commit automation (commits titled `[Auto] Pending changes committed <ts>`). This branch snapshots whatever is dirty in the live working tree — which can be **behind origin/main**. On 2026-06-12 its `scripts/deploy.sh` was the OLD buggy `PROD_PORT=8643` version (and it deleted `tests/test_deploy_port_defaults.py`) — i.e. those local commits would have **UNDONE** the just-merged #611 fix had they reached main.

**Rule:** before forcing `auto/commit-pending` (or any auto-commit branch) forward, **content-diff each commit vs origin/main** (`git diff origin/main -- <file>`), don't trust commit messages or the squash-merge detector (it matches by message and misses content-identical-but-renamed cases). Drop commits that revert merged work; cherry-pick only genuinely-new content.

## `/integrate` on the live `~/.hermes` — safe recipe

`integrate.sh --force` switches to local `main`, merges origin/main (force-resolves divergence), then creates a fresh `dev<ts>` branch. It does NOT delete branches with unmerged commits, so `auto/commit-pending` stays recoverable for cherry-pick. After integrate: verify `deploy.sh` is the main version, re-apply any genuinely-new `workspace/SOUL.md` rule, confirm the root `SOUL.md` symlink is intact. Related: [[coderabbit-dismissed-stuck-admin-override]].
