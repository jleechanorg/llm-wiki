---
title: "no-auto-flush config (Beads CLI)"
type: concept
tags: [beads, br, jsonl, dark-factory, worldai, pre-commit, config]
last_updated: 2026-07-04
---

# no-auto-flush config (Beads CLI)

## Definition

A configuration setting in `.beads/config.yaml` that disables `br`'s automatic `sync --flush-only` behavior on every command (`br create`, `br close`, `br update`, etc.). With this setting, the JSONL only updates when the operator explicitly invokes `br sync --flush-only`.

```yaml
issue-prefix: jleechan
no-db: false
no-daemon: true
db: beads.db
sync-branch: beads-sync
no-sparse-checkout: true
max-hash-length: 64
no-auto-flush: true
```

## Why it matters

The default `br` behavior auto-emits the entire SQLite DB to `.beads/issues.jsonl` on every command. On a feature branch with even a slightly different DB ordering, this produces a **+1663/-1663 wholesale PR diff** — every line position shifts even when only one record changed. The fix is to stop the auto-flush; the JSONL only updates when the operator deliberately wants to commit bead data.

## When it was introduced

- **2026-06-04**: worldarchitect.ai PR [#7270](https://github.com/jleechanorg/worldarchitect.ai/pull/7270) (commit `380f1b5ee4`) landed `no-auto-flush: true` on worldai
- **2026-07-04**: dark-factory PR [#137](https://github.com/jleechanorg/dark-factory/pull/137) (commit `36014b63985e`) mirrored the same config to dark-factory

## Companion patterns

The `no-auto-flush` setting is **layer 1** of the 3-layer defense in depth:

1. **`no-auto-flush: true`** (this concept) → prevents auto-flush churn
2. **Pre-commit auto-sorter** → canonicalizes JSONL by id before every commit (when the operator does flush deliberately)
3. **CI guard** → fails PRs that introduce unsorted JSONL

See [[BeadPrBridge]] for the full architecture.

## Operator runbook

After a fresh clone:

```bash
grep no-auto-flush .beads/config.yaml
# should print: no-auto-flush: true

# If missing (older clones or worktrees that predate the fix):
# 1. Open a PR adding `no-auto-flush: true` to .beads/config.yaml
# 2. Discard any JSONL churn in the working tree: git checkout -- .beads/issues.jsonl
# 3. Future `br create`/`br close` will no longer touch the JSONL
```

## How to flush deliberately

```bash
br sync --flush-only
# Only when you actually want the JSONL updated.
```

## References

- worldai memory: `feedback_2026-06-05_beads_no_auto_flush_stops_jsonl_churn.md`
- Source page: [[project-2026-07-04-bead-bridge-complete-architecture-and-pitfalls]]
- Upstream issue: [beads_rust #3474](https://github.com/Dicklesworthstone/beads_rust/issues/3474) — same root cause, same fix philosophy