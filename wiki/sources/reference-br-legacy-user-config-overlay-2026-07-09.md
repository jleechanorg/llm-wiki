---
title: "br v0.2.16 Legacy User-Config Overlay + no-auto-flush Drift"
date: 2026-07-09
type: reference
tags: [beads, br-cli, config, troubleshooting]
bead: jleechan-zlaw
related_concepts: [BrLegacyUserConfigOverlay, BrNoAutoFlushDrift]
related_entities: [BrCLI]
---

## Summary

`br` v0.2.16 silently overlays `~/.beads/config.yaml` as a "legacy user config" into
every cwd, shadowing project-level settings. Combined with `no-auto-flush: true`,
the home workspace at `/Users/jleechan/.beads` accumulated ~169 records of
DB↔JSONL drift that went unnoticed. Both root causes are now diagnosed and the
fix for #2 (auto-flush) was applied on 2026-07-09; the fix for #1 (prefix override)
is a one-liner after `br init`.

## Key Claims

- `br config path` reveals three resolution layers in order: `~/.config/beads/config.yaml`
  → `~/.beads/config.yaml` (legacy user config) → `<cwd>/.beads/config.yaml` (project).
  When the legacy layer exists, project settings are ignored unless they are
  explicitly uncommented in the project YAML.
- `br init` writes a *commented-out* template into the project's `.beads/config.yaml`:
  `# issue_prefix: br-sandbox-…`. Because the line is commented, the legacy overlay
  silently wins and every bead in that sandbox gets `jleechan-…` IDs.
- `no-auto-flush: true` causes br to write only to SQLite. The JSONL stays stale
  until `br sync --flush-only` is run explicitly. The home workspace had this
  flag set, and the first auto-flush after flipping it reconciled ~169 dirty records
  in a single shot.

## Key Quotes

> User config:        ~/.config/beads/config.yaml (not found)
> Legacy user config: ~/.beads/config.yaml         (found)   ← silently wins
> Project config:     <cwd>/.beads/config.yaml     (exists)  ← ignored while commented

## Connections

- [[BrCLI]] — the tool exhibiting the quirk
- [[BrLegacyUserConfigOverlay]] — the resolution-chain concept
- [[BrNoAutoFlushDrift]] — the auto-flush / drift concept

## Pre-flight Diagnostic Commands

```bash
br config path      # see the resolution chain
br config list      # confirm no_auto_flush: and prefix: resolved values
wc -l .beads/issues.jsonl && br count   # drift = JSONL lines vs DB count
```

## Fixes

**Fix 1 — auto-flush (applied 2026-07-09):**

```bash
# In /Users/jleechan/.beads/config.yaml, line 5:
#   no-auto-flush: true   →   no-auto-flush: false
# Backup: /Users/jleechan/.beads/config.yaml.bak.20260709-105524
```

**Fix 2 — per-project prefix override:**

```bash
# After `br init`, uncomment the template line:
sed -i.bak 's/^# issue_prefix:/issue_prefix:/' <cwd>/.beads/config.yaml
# Pre-fix edit path verified in /tmp/br-fix2-1783619767
```

## Verification Evidence

- Pre-fix JSONL line count: 116 (DB had ~285 records → 169-record drift)
- Post-fix JSONL line count after one `br create` + `br close` cycle: 285 lines
- Test bead `jleechan-rmp4` (created/closed during verification) in JSONL with
  matching status, closed_at, close_reason.
- Sandbox test `/tmp/br-fix2-1783619767`: pre-uncomment prefix = `jleechan-…`,
  post-uncomment prefix = `br-fix2-…`.

## Related Memory

- `~/.claude/projects/-Users-jleechan/memory/reference_br_legacy_user_config_overlay.md`
  (Claude auto-memory with the same content, indexed in MEMORY.md)

## References

- Repo: https://github.com/Dicklesworthstone/beads_rust
- Latest stable at install time: `v0.2.16` (2026-06-29)
- Bead: jleechan-zlaw (closed 2026-07-09)
- Roadmap: `~/roadmap/learnings-2026-07.md` (entry: "br legacy user-config overlay + auto-flush drift")
- Sibling sources: `sources/br-cli-bead-access-pattern-2026-05-14.md` (the br CLI access pattern)