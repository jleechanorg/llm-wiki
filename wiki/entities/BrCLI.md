---
title: "BrCLI"
type: entity
tags: [beads, issue-tracker, rust-cli]
sources:
  - sources/br-cli-bead-access-pattern-2026-05-14.md
  - sources/reference-br-legacy-user-config-overlay-2026-07-09.md
  - sources/pr-6-chore-migrate-beads-to-br-sqlite-isolated.md
  - sources/pr-62-migrate-migrate-beads-to-beads-rust-br-sqlite-work.md
last_updated: 2026-07-09
---

## Overview

`br` is the Rust-based issue tracker CLI from https://github.com/Dicklesworthstone/beads_rust.
Replaced the Python `bd` workflow for most jleechanorg beads operations.
SQLite is the primary store (`beads.db`); JSONL (`issues.jsonl`) is the export/sync
artifact. v0.2.16 is the latest stable as of 2026-07-09.

## Key Properties

- **Direct mode default**: `BEADS_USE_DAEMON=0` env, `Daemon: not connected` in `br info`.
- **Config-resolution quirk**: reads `~/.beads/config.yaml` as a legacy user-config
  overlay for *any* cwd, shadowing project configs that have commented-out templates.
  See [[BrLegacyUserConfigOverlay]].
- **No-auto-flush behavior**: with `no-auto-flush: true`, JSONL stays stale until
  `br sync --flush-only` runs. See [[BrNoAutoFlushDrift]].
- **Issue-prefix resolution**: follows the same overlay chain; per-project prefix
  requires uncommenting the template after `br init`.

## Subcommands (canonical set, v0.2.16)

`agents · audit · blocked · capabilities · changelog · close · comments · completions ·
config · coordination · count · create · defer · delete · dep · doctor · epic · gate ·
graph · history · info · init · label · lint · list · orphans · q · query · ready ·
reopen · robot-docs · show · stats · sync · update · upgrade · version`

## Idiomatic Usage

```bash
br show <id>          # single bead detail (preferred over reading JSONL)
br search <term>      # full-text search
br list --status open # filtered list
br count              # summary counts
br sync --flush-only  # export DB → JSONL (only when auto-flush is off)
br sync --status      # check JSONL ↔ DB drift without mutating
```

## Related Concepts

- [[BrLegacyUserConfigOverlay]]
- [[BrNoAutoFlushDrift]]

## References

- Memory: `~/.claude/projects/-Users-jleechan/memory/reference_br_legacy_user_config_overlay.md`
- Roadmap: `~/roadmap/learnings-2026-07.md` entry "br legacy user-config overlay + auto-flush drift"
- Source page: `sources/reference-br-legacy-user-config-overlay-2026-07-09.md`