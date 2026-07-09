---
title: "BrNoAutoFlushDrift"
type: concept
tags: [beads, config, data-integrity, troubleshooting]
sources:
  - sources/reference-br-legacy-user-config-overlay-2026-07-09.md
related_entities: [BrCLI]
last_updated: 2026-07-09
---

## Definition

When `~/.beads/config.yaml` contains `no-auto-flush: true` (hyphen form; br also
accepts the underscore form `no_auto_flush`), br writes new issues only to SQLite
(`beads.db`). The JSONL export (`issues.jsonl`) stays stale until
`br sync --flush-only` runs. Long-running configurations of this flag can
accumulate hundreds of "dirty" DB records with no JSONL counterpart.

## Symptom

- `wc -l .beads/issues.jsonl` is far smaller than `br count`.
- `br sync --status` shows the dirty backlog.
- Any tool that consumes only the JSONL (git diff review, external sync, dry-run
  exporters) sees a partial snapshot.

## Diagnostic

```bash
wc -l .beads/issues.jsonl          # current JSONL record count
br count                           # current DB record count
br sync --status                   # explicit dirty count
br config list | grep no_auto_flush
```

Drift = `br count` − `wc -l issues.jsonl`.

## Fix

Flip the flag in the project config:

```yaml
# /Users/jleechan/.beads/config.yaml, line 5:
no-auto-flush: false   # was: true
```

The first `br create` / `br close` / `br update` after flipping the flag will
flush the entire dirty backlog in a single transaction. With br's
atomic-temp-file-then-rename export pattern, this is safe even when the backlog
is large.

**FIX applied 2026-07-09**: `/Users/jleechan/.beads/config.yaml.bak.20260709-105524`
is the pre-fix backup; first post-fix flush reconciled 169 records (JSONL
116 → 285 lines) without manual intervention.

## Why It Matters

This drift is silent — no error message, no log line — and only surfaces when
someone consumes the JSONL for review or sync. For an audit trail relying on
JSONL as the source of truth (e.g. worldarchitect.ai PR review workflows), a
long `no-auto-flush: true` era can produce false confidence in the export's
completeness.

## Related Concepts

- [[BrLegacyUserConfigOverlay]] — the config-resolution sibling quirk
- [[BrCLI]] — the tool

## References

- Source page: `sources/reference-br-legacy-user-config-overlay-2026-07-09.md`
- Memory: `~/.claude/projects/-Users-jleechan/memory/reference_br_legacy_user_config_overlay.md`
- Pre-fix backup: `/Users/jleechan/.beads/config.yaml.bak.20260709-105524`